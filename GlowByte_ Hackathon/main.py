import re
import sys
import pickle
import holidays
import warnings
import numpy as np
import pandas as pd

from datetime import datetime

pd.set_option('max_columns', None)
warnings.filterwarnings("ignore")
datetime_format = "%d.%m.%Y %H:%M:%S"


def change(text, numbers=True):
    # удаляем в начале и в конце строки пробелы
    text = str(text).strip()
    text = text.replace('(', ' ')
    text = text.replace(')', ' ')
    text = str(text).strip()
    # убираем цифры и проценты
    if numbers is True:
        ex = re.sub(r'\d{1,}[,.]\d{1,}', '', text)
        ex = re.sub(r'\d{1,}%|\d{1,} %', '', ex)
        ex = re.sub(r'\d{1,}', '', ex)
        ex = re.sub(r'мм\w{0,}', '', ex)
    else:
        all_results = re.findall(r"\d{1,2}%|\d[.]\d|мм", text)
        if all_results:
            return 1

    # поиск и замена неполного слова
    ex = re.sub(r'\bобл[^с\W]\w{0,}|\bобл[^с\W]', 'облачно', ex)
    ex = re.sub(r'\bпа\w{0,}', 'пасмурно', ex)
    ex = re.sub(r'\bвет\w{0,}', 'ветер', ex)
    ex = re.sub(r'\bсн\w{0,}', 'снег', ex)
    ex = re.sub(r'\bпр\w{0,}', 'прояснения', ex)
    # пример с просто облачно
    ex = re.sub(r'\bоб\w{0,}[., ]{,2}с[ ]{0,1}п\w{0,}[. ]{0,2}|\bобл\w{0,}с[., ]{,2}[ ]{0,1}п\w{0,}[., ]{0,2}', 'облачно', ex)
    ex = re.sub(r'\bобл\w{0,}', 'облачно', ex)
    # пример с просто пасмурно
    ex = re.sub(r'\bпа\w{0,}[., ]{,2}с[ ]{0,1}пр\w{0,}[. ]{0,2}', 'пасмурно', ex)
    ex = re.sub(r'\bдо\w{0,}|\bд\b', 'дождь', ex)
    ex = re.sub(r'\bгра\w{0,}', 'град', ex)
    ex = re.sub(r'\bд\w{0,} {0,}в\w{0,} {0,}с\w{0,}', 'дождь,ветер,снег', ex)
    ex = re.sub(r'\bшт\w{0,}', 'шторм', ex)
    # пример с просто облачно
    ex = re.sub(r'\bп\w{0,}[./ ]{1,2}об\w{0,}|\bп\w{0,}[.,]{0,1}об\w{0,}[.,]{0,1}|\bп\w{0,}\.{0,1}/об\w{0,}\.{0,1}', 'облачно,', ex)
    # пример с облачно
    ex = re.sub(r'\bмалооб\w{0,}|\bмалоб\w{0,}', 'облачно', ex)
    ex = re.sub(r'\bгро\w{0,}', 'гроза', ex)
    ex = re.sub(r'\bд\w{0,}[ ]{0,2}\+с\w{0,}|\bс\w{0,}\+д\w{0,}', 'дождь,снег', ex)
    # пример с дождем
    ex = re.sub(r'\bлив\w{0,}', 'дождь', ex)
    ex = re.sub(r'\bморо[^з\W]\w{0,}', 'морось', ex)
    # вместо прояснения ясно
    ex = re.sub(r'\bпр\w{0,}', 'ясно', ex)
    # вместо солнечно ясно
    ex = re.sub(r'\bсолн\w{0,}', 'ясно', ex)

    # изменяем степени сравнения
    ex = re.sub(r'\bвоз\w{0,}', '', ex)
    ex = re.sub(r'\bнеб\w{0,}', '', ex)
    ex = re.sub(r'\bсл\w{0,}', '', ex)
    ex = re.sub(r'\bмес\w{0,}', '', ex)
    ex = re.sub(r'\bл[её]г\w{0,}', '', ex)
    ex = re.sub(r'\bсил\w{0,}', '', ex)
    ex = re.sub(r'\bвр\w{0,}', '', ex)
    ex = re.sub(r'\s\bсо\s', ',', ex)
    ex = re.sub(r'\bсев\w{0,}', '', ex)
    ex = re.sub(r'\bрас\w{0,}', '', ex)
    ex = re.sub(r'\bспл\w{0,}', '', ex)
    ex = re.sub(r'\bхол\w{0,}', '', ex)
    ex = re.sub(r'\bмел\w{0,}', '', ex)
    ex = re.sub(r'\bкр\w{0,}', '', ex)
    ex = re.sub(r'\bпуш\w{0,}', '', ex)
    ex = re.sub(r'\bхлоп\w{0,}', '', ex)
    ex = re.sub(r'\bкомф\w{0,}', '', ex)
    ex = re.sub(r'\bмокр\w{0,}', '', ex)
    ex = re.sub(r'\bмаст\w{0,}', '', ex)
    ex = re.sub(r'\bмин\w{0,}', '', ex)
    ex = re.sub(r'\bпор\w{0,}', '', ex)
    ex = re.sub(r'\bоч\w{0,}', '', ex)
    ex = re.sub(r'\bгус\w{0,}', '', ex)
    ex = re.sub(r'\bледя\w{0,}', '', ex)
    # пробуем убрать осадки
    ex = re.sub(r'\bосад\w{0,}', '', ex)
    # убираем восток
    ex = re.sub(r'\bвост\w{0,}', '', ex)
    # убираем на
    ex = re.sub(r'\bна\b', '', ex)
    # убираем в
    ex = re.sub(r'\bв\b', '', ex)
    # убираем без
    ex = re.sub(r'\bбез\b', '', ex)
    # убираем стено
    ex = re.sub(r'\bстен\w{0,}', '', ex)
    ex = re.sub(r'\bине\w{0,}\b', '', ex)
    # тк морось - это мелкий дождь
    ex = re.sub(r'\bморос\w{0,}\b', 'дождь', ex)
    # сыро
    ex = re.sub(r'\bсыр\w{0,}\b', '', ex)
    # тает
    ex = re.sub(r'\bтае\w{0,}\b', '', ex)
    # снег
    ex = re.sub(r'\b\w{0,}нег\b', 'снег', ex)
    # сыро
    ex = re.sub(r'\bвс[её]\b', '', ex)
    # тает
    ex = re.sub(r'\bтих\w{0,}\b', '', ex)
    # душно
    ex = re.sub(r'\bдуш\w{0,}\b', 'жарко', ex)
    # изморозь, замороз
    ex = re.sub(r'\b\w{0,}мороз\w{0,}\b', 'мороз', ex)
    # ясно
    ex = re.sub(r'\bясн\w{0,}\b', 'ясно', ex)
    # сухие
    ex = re.sub(r'\bсух\w{0,}\b', '', ex)
    # пурга
    ex = re.sub(r'\bпург\w{0,}\b', 'метель', ex)
    # дымка
    ex = re.sub(r'\bдымк\w{0,}\b', 'туман', ex)
    # затяж
    ex = re.sub(r'\bзатя\w{0,}\b', '', ex)
    # мухи
    ex = re.sub(r'\bмух\w{0,}\b', '', ex)
    # зябко
    ex = re.sub(r'\bзяб\w{0,}\b', 'мороз', ex)
    # жарко
    ex = re.sub(r'\bжар\w{0,}\b', 'тепло', ex)

    # изменеения запятых, пробелов и точек, которые не нужны.
    ex = ex.replace('/', ',')
    ex = ex.replace('!', '')
    ex = ex.replace('?', '')
    ex = ex.replace('.', ' ')
    ex = ex.replace(' ,', ',')
    ex = ex.replace(',,', ',')
    ex = re.sub(r'  ', ' ', ex)
    ex = re.sub(r'  ', ' ', ex)
    ex = ex.replace('-', '')
    ex = ex.replace(', , ', ',')
    ex = ex.strip()

    # проверка на кол-во знач.
    if len(ex) == 0:
        ex = str(0)
    # проверка ',' в конце/начале
    if ex[-1] == ',':
        ex = ex[:-1]
    if ex[0] == ',':
        ex = ex[1:]

    ex = re.sub(r' {0,},{1,} {0,}', ',', ex)
    ex = ex.strip()

    # замена с на ,
    ex = re.sub(r' с ', ' ', ex)

    # проверка на пропуски запятой у определенных слов
    answer = ''
    counter = 1
    for text in ex.split(','):
        if counter != len(ex.split(',')):
            dop = ','
            counter += 1
        else:
            dop = ''

        if re.search(r' [с] ', text):
            answer += text
        elif re.search(r'[а][я] [о][б]', text):
            answer += text
        elif re.search(r' ', text):
            answer += re.sub(r' ', ',', text)
        else:
            answer += text
        answer += dop

    if answer[-1] == 'с':
        answer = answer.replace(',с', '')
    # cортировка по алфавиту
    answer = sorted(set(answer.split(',')))
    answer = ','.join(answer)

    if numbers is True:
        spisok = ['дождь', 'снег', 'метель', 'град', 'поземка', 'шторм', 'гроза']
        for i in answer.split(','):
            if i in spisok:
                return 1
        return 0


def encode_cyclic_feature(value, max_value):
    angle = (2 * np.pi * value) / max_value
    return np.cos(angle), np.sin(angle)


def first_non_empty(x):
    '''
        Отбрасываем пустые значения
    '''
    non_empty_values = x.dropna()
    if len(non_empty_values) > 1:
        return non_empty_values.iloc[-2]
    else:
        return np.nan


def take_numbers(x):
    '''
        Добавление строк с процентом воздуха/влажности
    '''
    if isinstance(x, str) is False:
        return np.nan
    x = x.replace(' ', '')
    all_results = re.findall(r"\d{1,2}%", x)
    if all_results:
        return int(all_results[0][:-1])
    else:
        return np.nan


def processing_block_1(df: pd.DataFrame) -> pd.DataFrame:
    '''
        1) Загружаем df;
        2) Предобрабатываем данные(Заменяем пропуски);
        3) Из текстовых данных достаём значения о прогнозе %влажности;
        4) Исключаем текстовые признаки.
    '''
    df.rename(columns={'temp': 'temp_fact'}, inplace=True)
    df = df.sort_values(['date', 'time'], ascending=True)

    # Делаем замену пустых значений в temp_pred. Заменяем на первое не пустое за последние 5 дней из факта
    # Не включая текущий день
    df['weather_pred'] = df['weather_pred'].replace({'0': np.nan})
    df['temp_pred'] = np.where(df['weather_pred'].isna(), np.nan, df['temp_pred'])

    window_1 = 5
    tmp = df.groupby('time')['temp_fact'].rolling(window=window_1, min_periods=1).apply(first_non_empty).reset_index()
    tmp = tmp.rename(columns={'temp_fact': 'yeasterday_for_fillna_temp_fact'})

    df = df.merge(tmp, how='left', left_on=['time', df.index], right_on=['time', 'level_1'], suffixes=('', '_calc'))
    df.drop('level_1', axis=1, inplace=True)
    df['temp_pred'] = np.where(df['temp_pred'].isna(), df['yeasterday_for_fillna_temp_fact'], df['temp_pred'])

    df['weather_pred_probability_pecent'] = df['weather_pred'].apply(take_numbers)

    df['weather_pred_probability_pecent'] = df.groupby(['date'])['weather_pred_probability_pecent'].transform(lambda x: x.fillna(x.mean()))

    tmp = df.groupby('time')['weather_pred_probability_pecent'].rolling(window=1, min_periods=1).apply(first_non_empty).reset_index()
    tmp = tmp.rename(columns={'weather_pred_probability_pecent': 'yeasterday_for_fillna_weather_pred_probability_pecent'})

    df = df.merge(tmp, how='left', left_on=['time', df.index], right_on=['time', 'level_1'], suffixes=('', '_calc'))
    df.drop('level_1', axis=1, inplace=True)

    df['weather_pred_probability_pecent'] = np.where(df['weather_pred_probability_pecent'].isna(), df['yeasterday_for_fillna_weather_pred_probability_pecent'], df['weather_pred_probability_pecent'])

    df['weather_fact'] = np.where(df['weather_fact'].isna(), df['weather_pred'], df['weather_fact'])
    df['weather_fact'] = np.where(df['weather_fact'].isna(), 'ясно', df['weather_fact'])

    df_fillna_pred_weater = df[['weather_fact', 'date', 'time']]
    df_fillna_pred_weater = df_fillna_pred_weater[df_fillna_pred_weater['time'] == 23]
    df_fillna_pred_weater['yeasterday_23_weater_fact_for_fillna'] = df_fillna_pred_weater['weather_fact'].shift(1)
    df_fillna_pred_weater = df_fillna_pred_weater[['date', 'yeasterday_23_weater_fact_for_fillna']]

    df = df.merge(df_fillna_pred_weater, how='left', on='date')

    df['weather_pred'] = np.where(df['weather_pred'].isna(), df['yeasterday_23_weater_fact_for_fillna'], df['weather_pred'])
    df['weather_pred'] = np.where(df['weather_pred'].isna(), 'ясно', df['weather_pred'])

    df['weather_pred'] = df['weather_pred'].apply(change)
    df['weather_fact'] = df['weather_fact'].apply(change)

    df.drop(['yeasterday_23_weater_fact_for_fillna'], axis=1, inplace=True)

    return df


def processing_block_2(df: pd.DataFrame) -> [pd.DataFrame, pd.DataFrame]:
    '''
        1) Формируем признаки сезонности
        2) Делаем pivot необходимых признаков
        3) Определяем признак периода дня и рабочего времени
        4) Определяем количество предстоящих праздников
    '''
    df['date'] = pd.to_datetime(df['date'])

    df_pivot = df.pivot(columns='time', index='date', values=['temp_pred', 'temp_fact', 'target'])

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['dayofweek'] = df['date'].dt.dayofweek
    df['weekofyear'] = df['date'].dt.weekofyear
    df['num_day_month'] = df['date'].dt.day

    df['datetime'] = pd.to_datetime(df['date']) + pd.to_timedelta(df['time'], unit='H')

    df['working_hour'] = np.where((df['time'] >= 9) & (df['time'] <= 17), 1, 0)
    df['day_period'] = np.where((df['time'] >= 4) & (df['time'] <= 11), 1,  # утро
                                np.where((df['time'] >= 12) & (df['time'] <= 16), 2,  # день
                                         np.where((df['time'] >= 17) & (df['time'] <= 23), 3,  # вечер
                                                  np.where((df['time'] >= 0) & (df['time'] <= 3), 0,  # ночь
                                                           None))))

    ru_holidays = holidays.RU()

    df_holidays_feature = df[['date']].drop_duplicates()

    df_holidays_feature['holidays_day'] = 0
    df_holidays_feature['cnt_holidays_3_days_immediate'] = 0

    df_holidays_feature.reset_index(drop=True, inplace=True)

    for i, date in enumerate(df_holidays_feature['date']):
        # Используем метод holidays.between для подсчета количества праздников в ближайших 5 днях
        if date in ru_holidays:
            df_holidays_feature.loc[i, 'holidays_day'] = 1
        for period in [3]:
            cnt_holidays = sum(1 for d in pd.date_range(date, periods=period) if d in ru_holidays)
            # Присваиваем полученное количество праздников в новый столбец
            df_holidays_feature.loc[i, f'cnt_holidays_{period}_days_immediate'] = cnt_holidays

    df = df.merge(df_holidays_feature, how='left', on=['date'])

    # Преобразование к синусу/косинусу
    df['month_sin'], df['month_cos'] = encode_cyclic_feature(df['month'], 12)
    df['dayofweek_sin'], df['dayofweek_cos'] = encode_cyclic_feature(df['dayofweek'], 7)
    df['weekofyear_sin'], df['weekofyear_cos'] = encode_cyclic_feature(df['weekofyear'], 52)
    df['num_day_sin'], df['num_day_cos'] = encode_cyclic_feature(df['num_day_month'], 30)

    df['hour_sin'], df['hour_cos'] = encode_cyclic_feature(df['time'], 24)

    df['day_off'] = np.where((df['dayofweek'] == 5) | (df['dayofweek'] == 6) | (df['holidays_day'] == 1), 1, 0)

    return df, df_pivot


def processing_block_3(df: pd.DataFrame, df_pivot: pd.DataFrame) -> pd.DataFrame:
    '''
        1) Считаем средний таргет за последние интервалы рабочего времени и времени отдыха.
        2) Считаем средний таргет за последние нерабочие дни.
        3) Объединяем эти данные в 1 пирзнак.
        4) Делаем признак таргета того же часа и температуры но за предыдущий день
        5) Прикрепляем статистические признаки(Общие из метеоданных)
        6) Делаем сдвиг на сутки в pivot таблице
        7) Удаляем вспомогательные колонки
    '''
    df_work_hour_work_day = df[df['day_off'] == 0].groupby(['date', 'working_hour'])['target'].mean().reset_index()
    df_work_hour_work_day = df_work_hour_work_day.sort_values(by='date')
    df_work_hour_work_day['last_target_work_period'] = df_work_hour_work_day.groupby('working_hour')['target'].shift(1)
    df_work_hour_work_day.drop('target', axis=True, inplace=True)

    df_day_off = df[df['day_off'] == 1]
    df_day_off = df_day_off.groupby('date')['target'].mean().reset_index()
    df_day_off['target_last_weekend'] = df_day_off['target'].shift(1)
    df_day_off.drop('target', axis=True, inplace=True)

    df = df.merge(df_work_hour_work_day, how='left', on=['date', 'working_hour'])
    df = df.merge(df_day_off, how='left', on=['date'])

    df['work_hour_weekend_last_days_stat'] = np.where(df['last_target_work_period'].isna(), df['target_last_weekend'], df['last_target_work_period'])
    df.drop(['last_target_work_period', 'target_last_weekend'], axis=1, inplace=True)

    df['previous_yeasterday_target_hour'] = df.groupby('time')['target'].shift(1)
    df['previous_yeasterday_temp_hour'] = df.groupby('time')['temp_fact'].shift(1)

    data_weater_stat = {
        'month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        'mean_temp_stat_month': [-0.4, 0.9, 3.7, 7.9, 12.5, 17.1, 18.6, 18.4, 13.9, 9.2, 5.1, 2.0],
        'humidity_stat_month': [87, 83, 78, 72, 70, 74, 77, 77, 82, 84, 89, 89],
        'wind_speed_stat_month': [4.3, 4.1, 3.8, 3.9, 3.8, 3.4, 3.5, 3.1, 3.3, 3.9, 3.9, 4.2],
        'number_days_clear_month': [3, 6, 8, 12, 12, 12, 9, 11, 11, 7, 3, 3],
        'number_days_cloudy_month': [21, 18, 17, 15, 15, 16, 19, 16, 16, 16, 21, 21],
        'number_days_mainly_cloudy_month': [5, 4, 4, 3, 2, 2, 2, 2, 3, 6, 4, 5],
        'number_days_rain_month': [2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 1, 2],
    }

    data_weater_stat_df = pd.DataFrame(data_weater_stat)

    df = df.merge(data_weater_stat_df, how='left', on='month')

    df_pivot_1 = df_pivot.copy()
    df_pivot_1.columns = [col[0] + '_' + str(col[1]) if len(col) == 2 else col for col in df_pivot_1.columns]
    df_pivot_1[[col for col in df_pivot_1.columns if 'pred' not in col]] = df_pivot_1[[col for col in df_pivot_1.columns if 'pred' not in col]].shift(1)

    df = df.merge(df_pivot_1, how='left', on='date')

    df.drop(['yeasterday_for_fillna_temp_fact', 'yeasterday_for_fillna_weather_pred_probability_pecent'], axis=1, inplace=True)

    return df


def processing_block_4(df: pd.DataFrame) -> pd.DataFrame:
    '''
        1) Считаем агредаты за вчерашний день;
        2) Добавляем бинарный признак is_higher, который указывает на рост или спад потребления относительно позавчерашнего дня
        по отношению к вчерашнему.
        3) Считаем статистики за каждый период вчерашнего дня(За утро, ночь, день и вечер)
    '''
    df['pecent_osad_pred'] = df.groupby('date')['weather_pred'].apply(lambda x: sum(x) / len(x))
    df['pecent_osad_fact_yeasterday'] = df.groupby('date')['weather_fact'].apply(lambda x: sum(x) / len(x)).shift(1)
    df_target_date = df.groupby('date').agg(target_day_sum=('target', 'sum'),
                                            target_day_mean=('target', 'mean'),
                                            temperature_fact_day_mean=('temp_fact', 'mean')
                                            ).reset_index()

    df_target_date['target_yesterday_day_sum'] = df_target_date['target_day_sum'].shift(1)
    df_target_date['target_yesterday_day_mean'] = df_target_date['target_day_mean'].shift(1)
    df_target_date['temp_fact_yesterday_day_mean'] = df_target_date['temperature_fact_day_mean'].shift(1)

    # Добавляем новый столбец 'is_higher'
    df_target_date['is_higher'] = (df_target_date['target_yesterday_day_mean'] > df_target_date['target_yesterday_day_mean'].shift()).astype(int)
    df_target_date.drop(['target_day_sum', 'target_day_mean', 'temperature_fact_day_mean'], axis=1, inplace=True)
    df = df.merge(df_target_date, how='left', on='date')

    df_group_period_day = df[['target', 'temp_fact', 'day_period', 'date']]

    df_group_period_day = df_group_period_day.groupby(['date', 'day_period'])['target', 'temp_fact'].agg(['mean']).reset_index()
    df_group_period_day.columns = [col[0] + '_' + col[1] if (col[0] != 'date') & (col[0] != 'day_period') else col[0] for col in df_group_period_day.columns]

    df_group_period_day = df_group_period_day.pivot(index='date', columns=['day_period'], values=['target_mean', 'temp_fact_mean']).reset_index()

    df_group_period_day.columns = [col[0] + '_' + str(col[1]) + '_' + 'easterday_day_period' if col[0] != 'date' else col[0] for col in df_group_period_day.columns]
    df_group_period_day[[col for col in df_group_period_day.columns if 'easterday_day_period' in col]
                        ] = df_group_period_day[[col for col in df_group_period_day.columns if 'easterday_day_period' in col]].shift(1)

    df = df.merge(df_group_period_day, how='left', on='date')

    return df


def processing_block_5(df, model, col_pred, mean_values) -> pd.DataFrame:
    columns_to_impute = col_pred.copy()
    df[columns_to_impute] = df[columns_to_impute].fillna(mean_values)
    df['predict'] = model.predict(df[col_pred])
    result_df = df[['datetime', 'predict']]
    return result_df


def main(path: str) -> pd.DataFrame:
    try:
        # Читаем тренировочные данные
        df = pd.read_csv(path)

        # Блок 1
        df = processing_block_1(df)

        # Блок 2
        df, df_pivot = processing_block_2(df)

        # Блок 3
        df = processing_block_3(df, df_pivot)

        # Блок 4
        df = processing_block_4(df)

        mean_values = pd.read_pickle('mean_values.pkl', compression='gzip')
        with open('col_pred.pkl', 'rb') as f:
            col_pred = pickle.load(f)
        with open('model_catboost.pkl', 'rb') as f:
            model = pickle.load(f)

        # Блок 5
        result_df = processing_block_5(df, model, col_pred, mean_values)

        result_df.to_csv('predict.csv', index=False)

        return result_df
    except Exception as e:
        str_log = f"{datetime.now().strftime(datetime_format)} main(): {e}"
        print(str_log)


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            main(sys.argv[1])
        else:
            print("The path is not set by the first parameter!")
            raise RuntimeError
    except Exception as e:
        str_log = f"{datetime.now().strftime(datetime_format)} __main__(): {e}"
        print(str_log)
