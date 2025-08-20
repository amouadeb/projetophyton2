import pandas as pd

def calculate_demographic_data(print_data=True): # imprime resultados necessarios do projeto

    # Read data from file
    df = pd.read_csv(
        "adult.data.csv",
        header=None,
        names=[
            "idade","trabalho","peso_final","escolaridade","num_escolaridade","estado_civil",
            "ocupacao","relacionamento","raca","sexo","ganho_capital","perda_capital",
            "horas_por_semana","pais_origem","salario"
        ],
        

    )

    for c in ["idade","peso_final","num_escolaridade","ganho_capital","perda_capital","horas_por_semana"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
        # garante que sejam colunas numericas, e rejeita texto

    df = df[df["idade"].notna()].reset_index(drop=True)
    # apaga linhas vazias/perdidas dentro do codigo

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df["raca"].value_counts()

    # What is the average age of men?
    average_age_men = round(df[df["sexo"] == "Male"]["idade"].mean(), 1)

    # What is the percentage of people who have a Bachelor's degree?
    total_de_pessoas = df.count()['escolaridade']
    df_bacharelado = df[df['escolaridade'] == 'Bachelors']
    pessoas_com_bacharelado = df_bacharelado.count()['escolaridade']
    percentage_bachelors = round((pessoas_com_bacharelado/total_de_pessoas)*100, 2)
    #percentage_bachelors = round((df["escolaridade"] == "Bachelors").mean() * 100, 1)

    # with and without Bachelors, Masters, or Doctorate
    superior = df[
        (df["escolaridade"] == "Bachelors") |
        (df["escolaridade"] == "Masters") |
        (df["escolaridade"] == "Doctorate")
    ]
    nao_superior = df[
        (df["escolaridade"] != "Bachelors") &
        (df["escolaridade"] != "Masters") &
        (df["escolaridade"] != "Doctorate")
    ]

    # percentage with salary >50K
    higher_education_rich = round((superior[superior["salario"] == ">50K"].shape[0] / superior.shape[0]) * 100, 1)
    lower_education_rich = round((nao_superior[nao_superior["salario"] == ">50K"].shape[0] / nao_superior.shape[0]) * 100, 1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = int(df["horas_por_semana"].min())

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    min_trabalhadores = df[df["horas_por_semana"] == min_work_hours]
    rich_percentage = round((min_trabalhadores[min_trabalhadores["salario"] == ">50K"].shape[0] / min_trabalhadores.shape[0]) * 100, 1)

    # What country has the highest percentage of people that earn >50K?
    salario_pais = df.groupby("pais_origem")["salario"].value_counts(normalize=True).unstack()
    highest_earning_country = salario_pais[">50K"].idxmax()
    highest_earning_country_percentage = round(salario_pais[">50K"].max() * 100, 1)

    # Identify the most popular occupation for those who earn >50K in India.
    india_rico = df[(df["pais_origem"] == "India") & (df["salario"] == ">50K")]
    top_IN_occupation = india_rico["ocupacao"].value_counts().idxmax() if not india_rico.empty else None

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
