#!/usr/bin/env python3
"""
电力交易数据分析脚本（无可视化依赖）
适用于缺少matplotlib的服务器环境
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json

def analyze_power_data():
    """执行完整的电力交易数据分析"""
    print("="*60)
    print("电力交易数据分析报告")
    print("="*60)
    
    # 生成模拟数据
    np.random.seed(42)
    dates = pd.date_range('2024-01-01', periods=168, freq='H')  # 一周数据
    data = pd.DataFrame({
        'timestamp': dates,
        'price': np.random.normal(350, 80, 168).clip(100, 800).round(2),
        'volume': np.random.randint(800, 6000, 168),
        'load': np.random.normal(12000, 3000, 168).round(1)
    })
    
    # 添加周循环模式
    data['price'] = data['price'] * (1 + 0.1 * np.sin(2 * np.pi * data.index / 24))
    
    print(f"\n1. 数据概览")
    print(f"   数据期间: {data['timestamp'].min()} 至 {data['timestamp'].max()}")
    print(f"   数据点数: {len(data)}")
    print(f"   时间分辨率: 每小时")
    
    print(f"\n2. 价格分析")
    price_stats = {
        'mean': data['price'].mean(),
        'median': data['price'].median(),
        'std': data['price'].std(),
        'min': data['price'].min(),
        'max': data['price'].max(),
        'q1': data['price'].quantile(0.25),
        'q3': data['price'].quantile(0.75)
    }
    
    for key, value in price_stats.items():
        print(f"   {key:6s}: {value:8.2f} 元/MWh")
    
    # 识别价格尖峰（超过平均值2个标准差）
    price_mean = data['price'].mean()
    price_std = data['price'].std()
    price_spikes = data[data['price'] > price_mean + 2 * price_std]
    print(f"\n3. 价格尖峰检测")
    print(f"   检测阈值: {price_mean + 2 * price_std:.2f} 元/MWh")
    print(f"   发现尖峰: {len(price_spikes)} 次")
    
    if len(price_spikes) > 0:
        print(f"   尖峰时段:")
        for idx, row in price_spikes.head(3).iterrows():
            print(f"     {row['timestamp']}: {row['price']:.2f} 元/MWh")
    
    print(f"\n4. 负荷与价格相关性")
    correlation = data['price'].corr(data['load'])
    print(f"   相关系数: {correlation:.3f}")
    if correlation > 0.5:
        print("   → 强正相关: 负荷增加时电价通常上涨")
    elif correlation < -0.5:
        print("   → 强负相关: 负荷增加时电价通常下降")
    else:
        print("   → 弱相关: 负荷与电价关系不明显")
    
    print(f"\n5. 交易量分析")
    print(f"   总交易量: {data['volume'].sum():,} MWh")
    print(f"   平均小时交易量: {data['volume'].mean():.0f} MWh")
    
    # 按小时分析
    data['hour'] = data['timestamp'].dt.hour
    hourly_stats = data.groupby('hour').agg({
        'price': 'mean',
        'volume': 'mean',
        'load': 'mean'
    }).round(2)
    
    print(f"\n6. 分时统计（高峰/低谷）")
    peak_hour = hourly_stats['price'].idxmax()
    valley_hour = hourly_stats['price'].idxmin()
    print(f"   电价高峰时段: {peak_hour:02d}:00 ({hourly_stats.loc[peak_hour, 'price']:.2f} 元/MWh)")
    print(f"   电价低谷时段: {valley_hour:02d}:00 ({hourly_stats.loc[valley_hour, 'price']:.2f} 元/MWh)")
    
    # 保存分析结果
    print(f"\n7. 保存结果文件")
    
    # 保存CSV
    data.to_csv('power_analysis_results.csv', index=False)
    print(f"   ✓ 完整数据: power_analysis_results.csv")
    
    # 保存JSON摘要
    summary = {
        'analysis_time': datetime.now().isoformat(),
        'period': {
            'start': data['timestamp'].min().isoformat(),
            'end': data['timestamp'].max().isoformat()
        },
        'price_statistics': {k: round(v, 2) for k, v in price_stats.items()},
        'correlation': round(correlation, 3),
        'total_volume': int(data['volume'].sum()),
        'peak_hour': int(peak_hour),
        'valley_hour': int(valley_hour)
    }
    
    with open('analysis_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"   ✓ 分析摘要: analysis_summary.json")
    
    # 生成文本报告
    with open('analysis_report.txt', 'w') as f:
        f.write("="*60 + "\n")
        f.write("电力交易数据分析报告\n")
        f.write("="*60 + "\n\n")
        f.write(f"分析时间: {datetime.now()}\n")
        f.write(f"数据期间: {data['timestamp'].min()} 至 {data['timestamp'].max()}\n")
        f.write(f"平均电价: {price_stats['mean']:.2f} 元/MWh\n")
        f.write(f"价格波动率: {(price_stats['std']/price_stats['mean']):.1%}\n")
        f.write(f"价格尖峰次数: {len(price_spikes)}\n")
        f.write(f"总交易量: {data['volume'].sum():,} MWh\n")
    
    print(f"   ✓ 文本报告: analysis_report.txt")
    print(f"\n" + "="*60)
    print("分析完成！已生成3个输出文件")
    print("="*60)

if __name__ == "__main__":
    analyze_power_data()

##以下的改动是用来测试
