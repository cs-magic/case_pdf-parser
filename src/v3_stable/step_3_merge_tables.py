import pandas as pd
from sqlalchemy import select, null

from src.database import get_db
from src.log import logger
from src.models import Paper
from src.utils.dataframe import data2df, df2data
from src.utils.find_longest_subsequence import find_longest_subsequence
from src.utils.preprocess_table import preprocess_array


def merge_tables(paper: Paper) -> Paper:
    tables = paper.criterion_tables
    assert len(tables) > 0, paper
    all_pages = [table.page for table in tables]
    logger.info(f'all_pages : {all_pages}')
    target_page_index_list = find_longest_subsequence(all_pages, True)
    start_page = all_pages[target_page_index_list[0]]
    end_page = all_pages[target_page_index_list[-1]]
    df_list = [data2df(preprocess_array(tables[index].raw_data)) for index in target_page_index_list]
    df = df_list[0]
    for right_df in df_list[1:]:
        df = pd.concat([df, right_df], axis=0)
    logger.info(f'merged tables:\n{df.to_markdown(tablefmt="grid")}')
    data = df2data(df)
    paper.merged_tables_count = len(df_list)
    paper.merged_rows_count = len(data)
    paper.merged_criterion_table = data
    paper.merged_table_start_page = start_page
    paper.merged_table_end_page = end_page
    return paper


def step_3_merge_tables():
    with get_db() as session:
        query = select(Paper).where(
            # Paper.merged_criterion_table == null(), # 更新所有没有跑表的
            Paper.criterion_tables_count != null(), Paper.criterion_tables_count > 0)
        papers = session.scalars(query).all()
        logger.info(f'papers count={len(papers)}')
        for (index, paper) in enumerate(papers[:]):
            logger.info(f"handling [{index} / {len(papers)}] paper: {paper}")

            paper = merge_tables(paper)

            session.add(paper)
            session.commit()


if __name__ == '__main__':
    step_3_merge_tables()
