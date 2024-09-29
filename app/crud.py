import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import ConsumptionEntry, ConsumptionDevice, UserInfo
import database


def get_all_data(db: Session):
    """Obtiene todos los registros de consumo, información del usuario y nivel de consumo del dispositivo."""
    # Query para obtener datos de consumo, información del usuario y nivel de consumo del dispositivo
    query = (
        db.query(
            ConsumptionEntry.user_id,
            ConsumptionEntry.consumption_value,
            ConsumptionEntry.device_id,
            ConsumptionEntry.start_time,
            ConsumptionEntry.end_time,
            UserInfo.energy_behavior,
            UserInfo.number_occupant_living,
            UserInfo.housing_type,
            ConsumptionDevice.level_consumption
        )
        .join(UserInfo, ConsumptionEntry.user_id == UserInfo.user_id)
        .join(ConsumptionDevice, ConsumptionEntry.device_id == ConsumptionDevice.id)
    )
    return query.all()


if __name__ == "__main__":
    db_session = next(database.get_db())  # Obtén la sesión de base de datos
    try:
        # Obtener todos los registros con las uniones necesarias
        results = get_all_data(db_session)

        # Crear el DataFrame con los datos de las tres tablas
        data = {
            'user_id': [result.user_id for result in results],
            'valor_consumo': [result.consumption_value for result in results],
            'device_id': [result.device_id for result in results],
            'start_time': [result.start_time for result in results],
            'end_time': [result.end_time for result in results],
            'energy_behavior': [result.energy_behavior for result in results],
            'number_occupant_living': [result.number_occupant_living for result in results],
            'housing_type': [result.housing_type for result in results],
            'level_consumption': [result.level_consumption for result in results],
        }

        df = pd.DataFrame(data)
        #======================== PREPARAR LOS DATOS PARA EL MODELO 1========================
        
        df['time_use'] = df['end_time'] - df['start_time']
        df.drop(['start_time', 'end_time'], axis=1, inplace=True)  # Omitir columnas de tiempo si no las necesitas
        # Incluir características relevantes para el consumo
        features = ['device_id', 'user_id', 'time_use', 'level_consumption', 'number_occupant_living', 'energy_behavior', 'housing_type']

        # Seleccionar las variables dependientes (consumo y costo de energía)
        X = df[features]  # Variables independientes
        y_consumption = df['valor_consumo']  # Variable objetivo para predecir el consumo

        # Escalar las variables numéricas para evitar que dominen el entrenamiento
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X.select_dtypes(include=['float64', 'int64']))
        
        # Dividir los datos en conjuntos de entrenamiento y prueba
        X_train, X_test, y_train_consumption, y_test_consumption = train_test_split(X_scaled, y_consumption, test_size=0.2, random_state=42)
        
        #======================== ENTRENAR EL MODELO 1========================
        
        # Entrenar el modelo de consumo
        consumption_model = RandomForestRegressor(n_estimators=100, random_state=42)
        consumption_model.fit(X_train, y_train_consumption)

        # Predicciones
        y_pred_consumption = consumption_model.predict(X_test)

        # Evaluación del modelo
        mse_consumption = mean_squared_error(y_test_consumption, y_pred_consumption)
        r2_consumption = r2_score(y_test_consumption, y_pred_consumption)
        print(f"Mean Squared Error: {mse_consumption}")
        print(f"R-squared: {r2_consumption}")
        

        # ======================== GRAFICAR LAS PREDICCIONES DEL MODELO ========================

        plt.figure(figsize=(10, 6))

        # Graficar los valores reales vs los predichos
        plt.scatter(y_test_consumption, y_pred_consumption, color='blue', label='Predicciones')

        # Dibujar una línea de identidad para mostrar una predicción perfecta (valores reales = predichos)
        plt.plot([y_test_consumption.min(), y_test_consumption.max()], [y_test_consumption.min(), y_test_consumption.max()], color='red', lw=2, label='Valor perfecto')

        # Etiquetas y título
        plt.xlabel('Consumo Real (kWh)')
        plt.ylabel('Consumo Predicho (kWh)')
        plt.title('Comparación entre Consumo Real y Predicho')
        plt.legend()

        # Mostrar la gráfica
        plt.show()


        # Mostrar el DataFrame resultante
        #print(df)
        
        #======================== PREPARAR Y ENTRENAR EL MODELO 2========================
        
        # Añadir una columna de costo estimado (ejemplo, costo por kWh)
        df['energy_cost_per_unit'] = 737,6  # Este valor puede cambiar según el contexto

        # Crear variable objetivo para el costo estimado
        y_cost = df['valor_consumo'] * df['energy_cost_per_unit']

        # Dividir en conjunto de entrenamiento y prueba
        X_train_cost, X_test_cost, y_train_cost, y_test_cost = train_test_split(X_scaled, y_cost, test_size=0.2, random_state=42)

        # Entrenar el modelo para estimar costos
        cost_model = RandomForestRegressor(n_estimators=100, random_state=42)
        cost_model.fit(X_train_cost, y_train_cost)

        # Predicciones de costos
        y_pred_cost = cost_model.predict(X_test_cost)

        # Evaluación del modelo de costos
        mse_cost = mean_squared_error(y_test_cost, y_pred_cost)
        r2_cost = r2_score(y_test_cost, y_pred_cost)
        print(f"Mean Squared Error (Costos): {mse_cost}")
        print(f"R-squared (Costos): {r2_cost}")
        
        #========================graficar las predicciones del modelo 2========================
        plt.figure(figsize=(10, 6))
        plt.scatter(y_test_cost, y_pred_cost, alpha=0.5)
        plt.plot([min(y_test_cost), max(y_test_cost)], [min(y_test_cost), max(y_test_cost)], color='red', linestyle='--')  # Línea de referencia
        plt.title('Predicciones de Costo vs. Valores Reales')
        plt.xlabel('Costos Reales')
        plt.ylabel('Costos Predichos')
        plt.grid()
        plt.show()


    
    finally:
        db_session.close()  # Asegúrate de cerrar la sesión
