import pandas as pd
from code.database import get_engine

def create_map():
    """
    从数据库中查询餐厅统计数据，并保存为 CSV 文件。
    """
    # SQL 查询：统计每个国家的米其林餐厅信息
    query = """
    SELECT 
        c.iso_code,
        c.country,
        COUNT(*) AS total_michelin,
        SUM(CASE WHEN CAST(c.stars_label AS INTEGER) = 0 THEN 1 ELSE 0 END) AS zero_star,
        SUM(CASE WHEN CAST(c.stars_label AS INTEGER) = 1 THEN 1 ELSE 0 END) AS one_star,
        SUM(CASE WHEN CAST(c.stars_label AS INTEGER) = 2 THEN 1 ELSE 0 END) AS two_star,
        SUM(CASE WHEN CAST(c.stars_label AS INTEGER) = 3 THEN 1 ELSE 0 END) AS three_star
    FROM 
        cleaned_data_with_embeddings c
    GROUP BY 
        c.iso_code, c.country
    ORDER BY 
        total_michelin DESC;
    """
    
    # 获取数据库引擎
    engine = get_engine()

    try:
        # 从数据库查询数据
        with engine.connect() as connection:
            data = pd.read_sql(query, connection)

        # 可选：标准化国家名称（如果需要）
        data["country"] = data["country"].replace({
            "United States of America": "United States",
            "Russia": "Russian Federation",
            # 如果需要，可添加其他映射
        })

        # 保存结果到 CSV 文件
        output_file = "michelin_statistics_by_country.csv"
        data.to_csv(output_file, index=False)
        print(f"数据已保存到 {output_file}")

        # 返回 DataFrame 以便进一步处理
        return data

    except Exception as e:
        print("查询或保存数据时出错:", e)
        return None

