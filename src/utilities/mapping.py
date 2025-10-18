import os

import folium
import pandas as pd
from sqlalchemy import create_engine

from utilities.logger import logger


def rebuild_map(output_path: str) -> None:
    """
    Rebuilds the map and saves it to the specified output path.

    Args:
        output_path (str): The file path where the rebuilt map will be saved.
    """
    # Implementation of the map rebuilding logic goes here
    state_data = get_state_counts()
    url = "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/us-states.json"

    state_map = folium.Map(location=[40, -95], zoom_start=4)
    folium.Choropleth(
        geo_data=url,
        name="choropleth",
        data=state_data,
        columns=["state", "count"],
        key_on="feature.id",
        fill_color="YlGn",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Normalized PII Entries by State",
    ).add_to(state_map)
    state_map.save(output_path)


def get_state_counts() -> pd.DataFrame:
    """
    Retrieves the counts of normalized PII entries by state.

    Returns:
        pd.DataFrame: A DataFrame containing state counts.
    """
    # Implementation of the logic to get state counts goes here
    engine = create_engine(os.environ["DATABASE_URL"])
    sql = """
    with
        global_count as (
            select count(*) as global_count from public.normalized_pii_data
        )
    select 
        state, 
        (count(*) * 1.0 / global_count.global_count) as count 
    from public.normalized_pii_data 
    join global_count on true
    where state is not null 
    group by state, global_count.global_count;
    """

    with engine.connect() as conn:
        resp = pd.read_sql(sql=sql, con=conn)

    logger.debug(resp)

    return resp
