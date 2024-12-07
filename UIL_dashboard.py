import pandas as pd
import sqlite3
import re
import streamlit as st
import plotly as py
import altair as alt
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go


@st.cache_resource
def collect_dbs():
    # Create a SQLite connection
    conn = sqlite3.connect("uil.db")
    results_df = pd.read_sql_query("SELECT * FROM results", conn)
    pml_df = pd.read_sql_query("SELECT * FROM pml", conn)
    conn.close()

    return results_df, pml_df


def get_db(df):
    score_subset = [
        "concert_score_1",
        "concert_score_2",
        "concert_score_3",
        "concert_final_score",
        "sight_reading_score_1",
        "sight_reading_score_2",
        "sight_reading_score_3",
        "sight_reading_final_score",
    ]

    def fix_date(date):
        try:
            if isinstance(date, pd.Timestamp):
                new_date = date.strftime("%Y-%m-%d")
            else:
                new_date = date.split(" ")[0]
        except Exception as e:
            # Log the error or handle it as needed
            print(f"Error processing date: {date}, Error: {e}")
            new_date = date  # Return the original date if an error occurs
        return new_date

    df["contest_date"] = df["contest_date"].apply(fix_date)
    df["contest_date"] = pd.to_datetime(
        df["contest_date"], format="%Y-%m-%d", errors="coerce"
    )

    df["year"] = df["contest_date"].dt.year
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)

    # create event_search
    df["event_search"] = df["event"]
    # fix event col
    # create event_search
    df["event_search"] = df["event"]
    # fix event col
    df["event"] = df["event"].str.replace("tenor/bass chorus", "Tenor-Bass Chorus")
    df["event"] = df["event"].str.replace("mixed chorus", "Mixed Chorus")
    df["event"] = df["event"].str.replace("string orchestra", "String Orchestra")
    df["event"] = df["event"].str.replace("full orchestra", "Full Orchestra")
    df["event"] = df["event"].str.replace("treble chorus", "Treble Chorus")
    df["event"] = df["event"].str.title()
    # drop any rows where all scores are na
    df = df.dropna(subset=score_subset, how="all")

    # force numeric scores to be numeric
    df[score_subset] = df[score_subset].apply(pd.to_numeric, errors="coerce")

    # fill everything else with ""
    cols_not_in_subset = df.columns.difference(score_subset)
    df[cols_not_in_subset] = df[cols_not_in_subset].fillna("")

    df["song_concat"] = df["title_1"] + " " + df["title_2"] + " " + df["title_3"]
    df["composer_concat"] = (
        df["composer_1"] + " " + df["composer_2"] + " " + df["composer_3"]
    )
    # remove any non-alphanumeric characters and spaces
    df["song_concat"] = df["song_concat"].str.replace(r"[^\w\s]", "")
    df["song_concat"] = df["song_concat"].str.replace(" ", "")

    df["composer_concat"] = df["composer_concat"].str.replace(r"[^\w\s]", "")
    df["composer_concat"] = df["composer_concat"].str.replace(r" ", "")

    # make all characters lowercase
    df["song_concat"] = df["song_concat"].str.lower()
    df["composer_concat"] = df["composer_concat"].str.lower()

    # fix school names
    df["school_search"] = df["school"].str.strip().str.lower()
    df["school_search"] = df["school_search"].str.replace(r"[^\w\s]", "")
    df["school_search"] = df["school_search"].str.replace(r" ", "")

    return df


@st.cache_data(ttl=600)
def get_data():

    results_df, pml_df = collect_dbs()

    results_df = get_db(results_df)

    pml_df = clean_pml(pml_df)

    # fill na with 0
    results_df = results_df.fillna(0)

    results_df = results_df[results_df["concert_score_1"] != 0]
    results_df = results_df[results_df["concert_score_2"] != 0]
    results_df = results_df[results_df["concert_score_3"] != 0]
    results_df = results_df[results_df["concert_final_score"] != 0]
    results_df = results_df[results_df["sight_reading_score_1"] != 0]
    results_df = results_df[results_df["sight_reading_score_2"] != 0]
    results_df = results_df[results_df["sight_reading_score_3"] != 0]
    results_df = results_df[results_df["sight_reading_final_score"] != 0]

    # fix the sight reading score above 5 to just 5
    results_df.loc[
        results_df["sight_reading_final_score"] > 5, "sight_reading_final_score"
    ] = 5

    # change all concert scores to int
    results_df["concert_score_1"] = (
        results_df["concert_score_1"].astype(float).astype(int)
    )
    results_df["concert_score_2"] = (
        results_df["concert_score_2"].astype(float).astype(int)
    )
    results_df["concert_score_3"] = (
        results_df["concert_score_3"].astype(float).astype(int)
    )
    results_df["concert_final_score"] = (
        results_df["concert_final_score"].astype(float).astype(int)
    )
    results_df["sight_reading_score_1"] = (
        results_df["sight_reading_score_1"].astype(float).astype(int)
    )
    results_df["sight_reading_score_2"] = (
        results_df["sight_reading_score_2"].astype(float).astype(int)
    )
    results_df["sight_reading_score_3"] = (
        results_df["sight_reading_score_3"].astype(float).astype(int)
    )
    results_df["sight_reading_final_score"] = (
        results_df["sight_reading_final_score"].astype(float).astype(int)
    )

    # add columns called Choice 1, Choice 2, and Choice 3 where title and composer are combined
    results_df["choice_1"] = results_df["title_1"] + "–" + results_df["composer_1"]
    results_df["choice_2"] = results_df["title_2"] + "–" + results_df["composer_2"]
    results_df["choice_3"] = results_df["title_3"] + "–" + results_df["composer_3"]
    results_df.loc[:, "choice_1"] = results_df["choice_1"].str.title()
    results_df.loc[:, "choice_2"] = results_df["choice_2"].str.title()
    results_df.loc[:, "choice_3"] = results_df["choice_3"].str.title()

    results_df["school_level"] = ""
    results_df.loc[
        results_df["conference"].str.contains("A", na=False), "school_level"
    ] = "High School"
    results_df.loc[
        results_df["conference"].str.contains("C", na=False), "school_level"
    ] = "Middle School/JH"

    # change classification to title case
    results_df["classification"] = results_df["classification"].str.replace("-", " ")
    results_df["classification"] = results_df["classification"].str.title()
    results_df.loc[
        results_df["classification"].str.contains("Nv", na=False), "classification"
    ] = "Non Varsity"
    # if classification begins with "V" it is Varsit
    results_df.loc[
        results_df["classification"].str.contains(r"^V", na=False), "classification"
    ] = "Varsity"

    return results_df, pml_df


def clean_pml(pml):

    pml[["arranger", "composer", "specification"]] = pml[
        ["arranger", "composer", "specification"]
    ].fillna("")

    # only keep rows where event contains band, chorus, or orchestra
    pml = pml[
        pml["event_name"]
        .str.lower()
        .str.contains("band|chorus|orchestra|madrigal", na=False)
    ]

    # change fullorchestra to Full Orchestra
    pml.loc[:, "event_name"] = (
        pml.loc[:, "event_name"]
        .str.replace("fullorchestra", "Full Orchestra")
        .str.replace("mixedchorus", "Mixed Chorus")
        .str.replace("stringorchestra", "String Orchestra")
        .str.replace("tenorbasschorus", "Tenor-Bass Chorus")
        .str.replace("treblechorus", "Treble Chorus")
        .str.title()
    )

    # drop and steelband rows
    pml = pml[~pml["event_name"].str.contains("steelband", na=False)]

    # remove any rows where grade is not an int
    pml = pml[pml["grade"].isna() == False]

    # make sure grade is int
    try:
        # Convert "grade" to float, filter out NaN values, then convert to int
        pml["grade"] = pml["grade"].astype(float)
        pml = pml[pml["grade"].notna()]
        pml["grade"] = pml["grade"].astype(int)
    except ValueError:
        pml["grade"] = pml["grade"].str.extract(r"(\d+)", expand=False)
        pml["grade"] = pml["grade"].astype(int)

    pml["song_search"] = pml["title"].str.lower()
    pml["song_search"] = pml["song_search"].str.replace(r"[^\w\s]", "")
    pml["song_search"] = pml["song_search"].str.replace(r" ", "")

    pml["composer_search"] = pml["composer"].str.lower() + pml["arranger"].str.lower()
    pml["composer_search"] = pml["composer_search"].str.replace(r"[^\w\s]", "")

    pml["total_search"] = (
        pml["song_search"] + pml["composer_search"] + pml["specification"]
    )
    pml["total_search"] = (
        pml["total_search"].str.replace(r"[^\w\s]", "", regex=True).str.lower()
    )
    pml["total_search"] = pml["total_search"].str.replace(r" ", "")
    # replace anything that is not a-z with ""
    pml["total_search"] = pml["total_search"].str.replace(r"[^a-zA-Z]", "", regex=True)

    # fill na with 0
    pml["performance_count"] = pml["performance_count"].fillna(0)

    return pml


def main():
    st.title("UIL Dashboard")

    st.write(
        "Welcome to the UIL Dashboard. This dashboard is designed to help track UIL Concert and Sight Reading results from the state of Texas."
    )

    st.page_link("pages/about.py", label="About the dashboard")

    results_df, pml_df = get_data()

    tab1, tab2 = st.tabs(["C&SR Results", "PML"])

    with tab1:
        st.write("Please select an event to begin.")

        # remove anywhere where concert_1 is not a number
        filter_df = results_df

        event_select = st.selectbox(
            "Select an event",
            ["Band", "Chorus", "Orchestra"],
            index=None,
        )

        if event_select:
            filter_df = filter_df[filter_df["gen_event"] == event_select]

            if event_select == "Chorus":
                # create new to select sub events
                sub_event_select = st.multiselect(
                    "Select a sub event",
                    filter_df[filter_df["event_search"].str.contains("chorus")]["event"]
                    .sort_values()
                    .unique(),
                    default=[],
                )

                if sub_event_select:
                    filter_df = filter_df[filter_df["event"].isin(sub_event_select)]

            with st.expander("Filter by schools"):

                school_select = st.text_input("Enter a school name", "")
                school_select = school_select.lower()
                school_select = re.sub(r"\s+", "", school_select)

                if school_select:
                    filter_df = filter_df[
                        filter_df["school_search"].str.contains(school_select, na=False)
                    ]

            with st.expander("Filter by Levels"):

                school_level_select = st.selectbox(
                    "Select a school level",
                    filter_df["school_level"].sort_values().unique(),
                    index=None,
                )

                if school_level_select:

                    filter_df = filter_df[
                        filter_df["school_level"].str.contains(
                            school_level_select, na=False
                        )
                    ]

                    conference_select = st.multiselect(
                        "Select a conference",
                        filter_df["conference"].sort_values().unique(),
                        default=[],
                    )
                    if conference_select:
                        filter_df = filter_df[
                            filter_df["conference"].isin(conference_select)
                        ]

                classification_select = st.selectbox(
                    "Select a classification",
                    filter_df["classification"].sort_values().unique(),
                    index=None,
                )

                if classification_select:
                    filter_df = filter_df[
                        filter_df["classification"] == classification_select
                    ]

            with st.expander("Filter by song name and composer"):
                song_name_input = st.text_input("Enter a song name", "")
                song_name_input = song_name_input.lower()
                song_name_input = re.sub(r"\s+", "", song_name_input)

                composer_name_input = st.text_input("Enter a composer name", "")
                composer_name_input = composer_name_input.lower()
                composer_name_input = re.sub(r"\s+", "", composer_name_input)

            # director_select = st.sidebar.text_input("Enter a director name", "")
            # director_select = director_select.lower()

            # if director_select:

            #     filter_df = filter_df[filter_df["Director_search"].str.contains(director_select, na=False)]

            year_select = st.slider("Year Range", 2005, 2024, (2005, 2024))

            if year_select:
                filter_df = filter_df[
                    filter_df["year"].between(int(year_select[0]), int(year_select[1]))
                ]

            if song_name_input or composer_name_input:
                # only show rows where song name is in song_concat
                filter_df = results_df[
                    results_df["song_concat"].str.contains(song_name_input, na=False)
                ]
                # only show rows where composer name is in composer_concat
                filter_df = filter_df[
                    filter_df["composer_concat"].str.contains(
                        composer_name_input, na=False
                    )
                ]

            # format year
            filter_df["year"] = filter_df["year"].astype(int)
            filter_df = filter_df[
                [
                    "year",
                    "event",
                    "school",
                    "director",
                    "additional_director",
                    "classification",
                    "choice_1",
                    "choice_2",
                    "choice_3",
                    "concert_final_score",
                    "sight_reading_final_score",
                ]
            ]

            # shown_df = filter df with proper case and no underscores
            shown_df = filter_df.copy()
            shown_df.columns = shown_df.columns.str.replace("_", " ").str.title()

            st.write("Filtered Data")

            # hide index

            st.dataframe(
                shown_df,
                hide_index=True,
                column_config={
                    "Year": st.column_config.NumberColumn(format="%.0f"),
                },
            )

            # write len
            st.write("Number of rows:", len(filter_df))

            # make a scores over time
            st.write("Concert Scores Over Time")
            scores_over_time_c = (
                filter_df.groupby("year")["concert_final_score"].mean().sort_index()
            )

            print(filter_df.groupby("year")["concert_final_score"].mean().sort_index())

            scores_over_time_c2 = (
                results_df[results_df["gen_event"].str.contains(event_select)]
                .groupby("year")["concert_final_score"]
                .mean()
                .sort_index()
            )

            line_chart_c = go.Figure(
                data=[
                    go.Scatter(
                        x=scores_over_time_c.index,  # Use the index of the series
                        y=scores_over_time_c.values,
                        mode="lines",
                        name="Selected Results",
                        line=dict(color="#FF4B4B", width=2),
                    ),
                    go.Scatter(
                        x=scores_over_time_c2.index,  # Use the index of the series
                        y=scores_over_time_c2.values,
                        mode="lines",
                        name="All Results",
                        line=dict(color="#184883", width=2),
                    ),
                ]
            )

            line_chart_c.update_yaxes(autorange="reversed")

            # Update layout to optimize the legend for mobile
            line_chart_c.update_layout(
                legend=dict(
                    orientation="h",  # Horizontal legend
                    yanchor="bottom",  # Align legend at the bottom
                    y=0,  # Position the legend at the bottom
                    xanchor="right",  # Align legend to the right
                    x=1,  # Position legend to the right
                    font=dict(size=10),  # Smaller font size
                    bgcolor="rgba(255, 255, 255, 0.5)",  # Transparent background
                ),
                margin=dict(l=20, r=20, t=20, b=20),  # Compact margins
            )

            st.plotly_chart(line_chart_c)

            st.write("Sight Reading Scores Over Time")
            scores_over_time_sr = filter_df.groupby("year")[
                "sight_reading_final_score"
            ].mean()

            scores_over_time_sr2 = (
                results_df[results_df["gen_event"].str.contains(event_select)]
                .groupby("year")["sight_reading_final_score"]
                .mean()
                .sort_index()
            )

            line_chart_sr = py.graph_objs.Figure(
                data=[
                    py.graph_objs.Scatter(
                        x=scores_over_time_sr.index,
                        y=scores_over_time_sr.values,
                        mode="lines",
                        name="Selected Results",
                        line=dict(color="#FF4B4B", width=2),
                    ),
                    py.graph_objs.Scatter(
                        x=scores_over_time_sr2.index,
                        y=scores_over_time_sr2.values,
                        mode="lines",
                        name="All Results",
                        line=dict(color="#184883", width=2),
                    ),
                ],
            )

            line_chart_sr.update_yaxes(autorange="reversed")

            line_chart_sr.update_layout(
                legend=dict(
                    orientation="h",  # Horizontal legend
                    yanchor="bottom",  # Align legend at the bottom
                    y=0,  # Position the legend at the bottom
                    xanchor="right",  # Align legend to the right
                    x=1,  # Position legend to the right
                    font=dict(size=10),  # Smaller font size
                    bgcolor="rgba(255, 255, 255, 0.5)",  # Transparent background
                ),
                margin=dict(l=20, r=20, t=20, b=20),  # Compact margins
            )

            st.plotly_chart(line_chart_sr, key="line_chart_sr")

            # create a pie chart of the concert scores
            st.write("Concert Scores")
            concert_scores = filter_df["concert_final_score"].value_counts()
            pie_chart_c = py.graph_objs.Figure(
                data=[
                    py.graph_objs.Pie(
                        labels=concert_scores.index,
                        values=concert_scores.values,
                        hole=0.5,
                    )
                ]
            )
            st.plotly_chart(pie_chart_c, key="pie_chart_c")

            sight_reading_scores = filter_df["sight_reading_final_score"].value_counts()
            st.write("Sight Reading Scores")
            pie_chart_SR = py.graph_objs.Figure(
                data=[
                    py.graph_objs.Pie(
                        labels=sight_reading_scores.index,
                        values=sight_reading_scores.values,
                        hole=0.5,
                    )
                ]
            )
            st.plotly_chart(pie_chart_SR, key="pie_chart_SRresults")

        # # write len
        # st.write("Number of rows:", len(df))

    with tab2:
        st.write("PML")
        st.write("Select a title to show more information.")

        unfiltered_pml = pml_df
        filtered_pml = unfiltered_pml

        grade_select = st.slider(
            "Select a grade",
            0,
            6,
            (0, 6),
        )
        # filter by grade
        if grade_select:
            filtered_pml = filtered_pml[
                (filtered_pml["grade"] >= grade_select[0])
                & (filtered_pml["grade"] <= grade_select[1])
            ]

        song_name_input = st.text_input("Search Titles or Composers", "")
        song_name_input = song_name_input.lower()
        song_name_input = re.sub(r"[^\w\s]", "", song_name_input)
        # remove anything that is not a-z
        song_name_input = re.sub(r"[^a-zA-Z]", "", song_name_input)

        if song_name_input:
            filtered_pml = filtered_pml[
                filtered_pml["total_search"].str.contains(song_name_input, na=False)
            ]

        event_name_select = st.selectbox(
            "Select an event",
            filtered_pml["event_name"].sort_values().unique(),
            index=None,
        )

        if event_name_select:
            filtered_pml = filtered_pml[filtered_pml["event_name"] == event_name_select]

            if "chorus" in event_name_select.lower():
                accompaniment_select = st.selectbox(
                    "Select accompaniment",
                    options=["Both", "A Capella", "Accompanied"],
                )
                accompt_dict = {"A Capella": "(a cappella)", "Accompanied": "(accomp)"}

                if accompaniment_select != "Both":
                    filtered_pml = filtered_pml[
                        filtered_pml["specification"].str.contains(
                            accompt_dict[accompaniment_select], na=False
                        )
                    ]

        min_performance_count = st.slider(
            "Minimum Performance Count",
            0,
            100,
            0,
        )

        if min_performance_count:
            filtered_pml = filtered_pml[
                filtered_pml["performance_count"] >= min_performance_count
            ]

        # only keep columns
        display_pml = filtered_pml[
            [
                "grade",
                "event_name",
                "title",
                "composer",
                "arranger",
                "code",
                "performance_count",
                "average_concert_score",
                "average_sight_reading_score",
                "song_score",
                "specification",
            ]
        ]

        display_pml = display_pml.sort_values(by="code")

        # Create a copy of the column names with replacements
        display_columns = [col.replace("_", " ").title() for col in display_pml.columns]

        # Display the dataframe with modified column names
        pml_write = st.dataframe(
            display_pml.rename(columns=dict(zip(display_pml.columns, display_columns))),
            column_config={
                "Song Score": st.column_config.NumberColumn(
                    help="Rating based on average scores compared by year and performance count",
                    format="%.2f",
                )
            },
            selection_mode="single-row",
            on_select="rerun",
            hide_index=True,
        )

        if pml_write:
            selected_row = display_pml.iloc[pml_write.selection["rows"]]

        graphed_pml = filtered_pml[
            # no nan values
            (filtered_pml["average_concert_score"].notna())
            & (filtered_pml["average_sight_reading_score"].notna())
            # no zeros
            & (filtered_pml["average_concert_score"] != 0)
            & (filtered_pml["average_sight_reading_score"] != 0)
            & (filtered_pml["performance_count"] > 10)
        ]

        if graphed_pml[graphed_pml["performance_count"] > min_performance_count].empty:
            st.write("No data to graph")
            return

        else:

            if selected_row.empty:
                max_x = graphed_pml[
                    graphed_pml["performance_count"] > min_performance_count
                ]["average_concert_score"].max()
                max_y = graphed_pml[
                    graphed_pml["performance_count"] > min_performance_count
                ]["average_sight_reading_score"].max()

                bubble_chart_altair = (
                    alt.Chart(
                        graphed_pml[
                            graphed_pml["performance_count"] > min_performance_count
                        ]
                    )
                    .mark_circle()
                    .encode(
                        x=alt.X(
                            "average_concert_score",
                            scale=alt.Scale(type="log", domain=(1, max_x)),
                        ),
                        y=alt.Y(
                            "average_sight_reading_score",
                            scale=alt.Scale(type="log", domain=(1, max_y)),
                        ),
                        color=alt.Color("event_name", legend=None),
                        size=alt.Size(
                            "performance_count",
                            legend=None,
                            scale=alt.Scale(range=[2, 3000]),
                        ),
                        tooltip=[
                            "title",
                            "composer",
                            "event_name",
                            "average_concert_score",
                            "average_sight_reading_score",
                        ],
                    )
                    .interactive()
                )

                st.altair_chart(
                    bubble_chart_altair,
                    use_container_width=True,
                )

        if not selected_row.empty and selected_row["performance_count"].iloc[0] != 0:
            selected_code = str(selected_row["code"].values[0])
            full_title_info = pml_df[pml_df["code"] == selected_code]
            remaining_composer = full_title_info["composer"].values[0]
            remaining_title = full_title_info["title"].values[0]
            earliest_year = int(full_title_info["earliest_year"].values[0])
            grade = int(full_title_info["grade"].values[0])

            st.write(f"Data for {remaining_title} by {remaining_composer}")

            # graph how many times it has been performed compared to all other songs in the event
            remaining_perf_count = selected_row["performance_count"].values[0]

            if not event_name_select:
                event_name_select = selected_row["event_name"].values[0]

            # line chart of performances over time
            perf_over_time = results_df[
                results_df["event"].str.contains(event_name_select)
                & (results_df["year"].astype(int) >= earliest_year)
                & (
                    (
                        results_df["code_1"].isin(
                            pml_df[pml_df["grade"] == grade]["code"]
                        )
                    )
                    | (
                        results_df["code_2"].isin(
                            pml_df[pml_df["grade"] == grade]["code"]
                        )
                    )
                    | (
                        results_df["code_3"].isin(
                            pml_df[pml_df["grade"] == grade]["code"]
                        )
                    )
                )
            ]

            all_perf_df = results_df[
                results_df["event"].str.contains(event_name_select)
                & (results_df["year"].astype(int) >= earliest_year)
                & (
                    (
                        results_df["code_1"].isin(
                            pml_df[pml_df["grade"] == grade]["code"]
                        )
                    )
                    | (
                        results_df["code_2"].isin(
                            pml_df[pml_df["grade"] == grade]["code"]
                        )
                    )
                    | (
                        results_df["code_3"].isin(
                            pml_df[pml_df["grade"] == grade]["code"]
                        )
                    )
                )
            ]

            song_performances = all_perf_df[
                (all_perf_df["code_1"] == selected_code)
                | (all_perf_df["code_2"] == selected_code)
                | (all_perf_df["code_3"] == selected_code)
            ]

            # Group by year and count the performances, then rename the column to 'count'
            song_performances_count = (
                song_performances.groupby("year").size().reset_index(name="count")
            )

            # Grouping and preparing data
            song_performances_avg_score = (
                song_performances.groupby("year")["concert_final_score"]
                .mean()
                .sort_index()
            )

            # Create a subplot with shared x-axis and two y-axes
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            # Add the 'count' bar chart (primary y-axis)
            fig.add_trace(
                go.Bar(
                    x=song_performances_count["year"],
                    y=song_performances_count["count"],
                    name="Performance Count",
                    marker_color="rgba(55, 83, 109, 0.7)",  # Color for bars
                ),
                secondary_y=False,
            )

            # Add the 'average concert score' line chart (secondary y-axis)
            fig.add_trace(
                go.Scatter(
                    x=song_performances_avg_score.index,
                    y=song_performances_avg_score,
                    mode="lines+markers",  # Adds markers to the line
                    name="Avg. Concert Score",
                    line=dict(color="rgb(26, 118, 255)"),  # Color for line
                ),
                secondary_y=True,
            )

            # Update layout with titles and legends
            fig.update_layout(
                title_text=f"Performances (Bar) and Avg. Concert Scores (Line) for {remaining_title}",
                showlegend=False,
                xaxis=dict(title="Year"),
            )

            # Update y-axis titles
            fig.update_yaxes(
                title_text="Performance Count", secondary_y=False, showgrid=False
            )
            min_value = song_performances_avg_score.max()
            fig.update_xaxes(showgrid=False)  # Disable gridlines across x-axis
            fig.update_yaxes(
                title_text="Avg. Concert Score",
                secondary_y=True,
                range=[min_value + 0.5, 0.5],
                autorange=False,
            )

            song_performances.columns = song_performances.columns.str.replace(
                "_", " "
            ).str.title()
            song_performances.loc[:, "Choice 1"] = song_performances[
                "Choice 1"
            ].str.title()
            song_performances.loc[:, "Choice 2"] = song_performances[
                "Choice 2"
            ].str.title()
            song_performances.loc[:, "Choice 3"] = song_performances[
                "Choice 3"
            ].str.title()

            # pie chart

            st.dataframe(
                song_performances[
                    [
                        "Year",
                        "School",
                        "Director",
                        "Classification",
                        "Choice 1",
                        "Choice 2",
                        "Choice 3",
                        "Concert Final Score",
                        "Sight Reading Final Score",
                    ]
                ],
                column_config={
                    "Year": st.column_config.NumberColumn(format="%.0f"),
                },
                hide_index=True,
            )

            # Display the combined chart
            st.plotly_chart(fig, key="combined_chart_pml")

            all_perf_count = all_perf_df.shape[0]

            # make a pie chart
            pie_remaining = px.pie(
                values=[
                    remaining_perf_count,
                    all_perf_count - remaining_perf_count,
                ],
                names=[
                    f"{remaining_title}",
                    f"All Other Songs in category since {earliest_year}",
                ],
                title=f"Share of {event_name_select} grade {grade} performances",
                color_discrete_sequence=["#184883", "#FF4B4B"],
            )

            # Update the layout to anchor the legend at the bottom
            pie_remaining.update_layout(
                legend=dict(
                    orientation="h",  # Horizontal legend
                    yanchor="bottom",  # Align legend at the bottom
                    y=-0.1,  # Position legend just below the chart
                    xanchor="center",  # Center the legend horizontally
                    x=0.5,  # Center the legend in the middle of the chart
                    font=dict(size=10),  # Optional: Adjust font size if needed
                    bgcolor="rgba(255, 255, 255, 0.1)",  # Optional: Transparent backgro
                ),
                margin=dict(l=20, r=20, t=100, b=50),  # Adjust margins if necessary
            )

            st.plotly_chart(pie_remaining)

    st.write(
        "This dashboard was created by [Blaine Cowen](mailto:blaine.cowen@gmail.com)"
    )
    # create buy me coffee image with link
    st.html(
        '<a href="https://www.buymeacoffee.com/blainecowen" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 36px !important;width: 136px !important;" ></a>'
    )


if __name__ == "__main__":
    main()
