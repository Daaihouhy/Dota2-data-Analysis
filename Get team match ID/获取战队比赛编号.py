#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOTA2战队比赛ID爬取程序

功能：
1. 接收用户输入的DOTA2战队名称
2. 通过OpenDota API获取该战队对应的Team ID
3. 构建战队比赛页面URL
4. 爬取页面中所有比赛ID
5. 将比赛ID导出为CSV格式文件

所需依赖：
- requests>=2.32.5
- pandas>=2.3.3
- lxml>=5.0.0
"""

import sys
import requests
import pandas as pd
from lxml import etree


def get_team_id(team_name):
    """
    根据战队名称获取Team ID
    
    Args:
        team_name (str): 战队名称
    
    Returns:
        int: 战队的Team ID，若未找到则返回None
    """
    try:
        # OpenDota API：获取所有战队列表，然后根据名称匹配
        url = "https://api.opendota.com/api/teams"
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        
        data = response.json()
        if data and isinstance(data, list):
            # 遍历所有战队，寻找名称匹配的战队
            for team in data:
                if 'name' in team and team_name.lower() in team['name'].lower():
                    return team['team_id']
            
            print(f"未找到名称为'{team_name}'的战队")
            return None
        else:
            print(f"未找到名称为'{team_name}'的战队")
            return None
    except requests.exceptions.RequestException as e:
        print(f"获取战队ID时发生网络错误：{e}")
        return None
    except (KeyError, IndexError, ValueError) as e:
        print(f"解析战队ID时发生错误：{e}")
        return None


def build_matches_url(team_id):
    """
    构建战队比赛页面URL
    
    Args:
        team_id (int): 战队的Team ID
    
    Returns:
        str: 战队比赛页面的URL
    """
    base_url = "https://www.opendota.com/teams/{team_id}/matches"
    return base_url.format(team_id=team_id)


def crawl_match_ids(team_id):
    """
    使用OpenDota API获取战队的所有比赛ID
    
    Args:
        team_id (int): 战队的Team ID
    
    Returns:
        list: 包含所有比赛ID的列表
    """
    try:
        # OpenDota API：获取战队的所有比赛
        url = f"https://api.opendota.com/api/teams/{team_id}/matches"
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        
        data = response.json()
        if data and isinstance(data, list):
            # 提取所有比赛ID
            match_ids = [match['match_id'] for match in data if 'match_id' in match]
            return match_ids
        else:
            print("未获取到比赛数据")
            return []
    except requests.exceptions.RequestException as e:
        print(f"获取比赛数据时发生网络错误：{e}")
        return []
    except (KeyError, IndexError, ValueError) as e:
        print(f"处理比赛ID时发生错误：{e}")
        return []


def export_to_csv(match_ids, team_name):
    """
    将比赛ID导出为CSV文件
    
    Args:
        match_ids (list): 包含比赛ID的列表
        team_name (str): 战队名称，用于生成文件名
    """
    if not match_ids:
        print("没有比赛ID可导出")
        return
    
    try:
        # 创建DataFrame
        df = pd.DataFrame({'match_id': match_ids})
        
        # 生成文件名
        filename = f"{team_name}_match_ids.csv"
        
        # 导出为CSV文件
        df.to_csv(filename, index=False, encoding='utf-8')
        
        print(f"成功导出{len(match_ids)}个比赛ID到文件：{filename}")
    except Exception as e:
        print(f"导出CSV时发生错误：{e}")


def main():
    """
    主函数
    """
    print("DOTA2战队比赛ID爬取程序")
    print("=" * 30)
    
    # 获取用户输入的战队名称
    team_name = input("请输入DOTA2战队名称：").strip()
    
    if not team_name:
        print("战队名称不能为空")
        return
    
    print(f"\n正在处理战队：{team_name}")
    
    # 1. 获取战队ID
    print("1. 正在获取战队ID...")
    team_id = get_team_id(team_name)
    
    if not team_id:
        print("无法获取战队ID，程序终止")
        return
    
    print(f"   成功获取战队ID：{team_id}")
    
    # 2. 构建比赛页面URL
    print("2. 正在构建比赛页面URL...")
    matches_url = build_matches_url(team_id)
    print(f"   成功构建URL：{matches_url}")
    
    # 3. 获取比赛ID
    print("3. 正在获取比赛ID...")
    match_ids = crawl_match_ids(team_id)
    
    if not match_ids:
        print("   未获取到任何比赛ID")
        return
    
    print(f"   成功获取到{len(match_ids)}个比赛ID")
    
    # 4. 导出为CSV文件
    print("4. 正在导出CSV文件...")
    export_to_csv(match_ids, team_name)
    
    print("\n程序执行完成！")


if __name__ == "__main__":
    main()
