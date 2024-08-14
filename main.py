import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx
import plotly.graph_objs as go
from tasks import fetch_linkedin_profile_task

def calculate_risk(profile_data):
    risk_factors = {
        'Experiencia': 0.1,
        'Numero de Contactos': 0.01,
        'Correo Electrónico': 2,
        'Ubicación': 0.5,
        'Titulo Profesional': 0.3,
    }

    try:
        riesgo = (
            profile_data.get('Experiencia', 0) * risk_factors['Experiencia'] +
            profile_data.get('Numero de Contactos', 0) * risk_factors['Numero de Contactos'] +
            profile_data.get('Correo Electrónico', 0) * risk_factors['Correo Electrónico'] +
            profile_data.get('Ubicación', 0) * risk_factors['Ubicación'] +
            len(profile_data.get('Titulo Profesional', '')) * risk_factors['Titulo Profesional']
        )
        return round(riesgo, 2)
    except Exception as e:
        print(f"Error al calcular el riesgo: {e}")
        return None

def calculate_disc(profile_data):
    try:
        D, I, S, C = 0, 0, 0, 0
        title = profile_data.get('headline', '').lower()
        if any(word in title for word in ["gerente", "director", "líder"]):
            D += 5
        if any(word in title for word in ["ventas", "marketing", "relaciones públicas"]):
            I += 5
        if any(word in title for word in ["recursos humanos", "soporte", "equipo"]):
            S += 5
        if any(word in title for word in ["analista", "ingeniero", "técnico"]):
            C += 5

        D += min(len(profile_data.get('positions', {}).get('values', [])), 5)
        I += min(profile_data.get('numConnections', 0) // 100, 5)

        return {'D': D, 'I': I, 'S': S, 'C': C}
    except Exception as e:
        print(f"Error al calcular DISC: {e}")
        return {'D': 0, 'I': 0, 'S': 0, 'C': 0}

def create_profile_dataframe(profiles):
    try:
        data = []
        for profile in profiles:
            disc_scores = calculate_disc(profile)
            data.append({
                'Nombre': f"{profile.get('firstName', '')} {profile.get('lastName', '')}",
                'Titulo Profesional': profile.get('headline', ''),
                'Experiencia': len(profile.get('positions', {}).get('values', [])),
                'Numero de Contactos': profile.get('numConnections', 0),
                'Ubicación': profile.get('location', {}).get('name', ''),
                'Correo Electrónico': 1 if profile.get('emailAddress') else 0,
                'Riesgo': calculate_risk(profile),
                'DISC': disc_scores
            })
        return pd.DataFrame(data)
    except Exception as e:
        print(f"Error al crear el DataFrame: {e}")
        return pd.DataFrame()

def visualize_risks(df):
    try:
        plt.figure(figsize=(10, 8))
        sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
        plt.title('Mapa de Calor de Riesgos de Exposición')
        plt.show()
    except Exception as e:
        print(f"Error al visualizar los riesgos: {e}")

def visualize_network(profiles):
    try:
        G = nx.Graph()
        for profile in profiles:
            node_name = f"{profile.get('firstName', '')} {profile.get('lastName', '')}"
            G.add_node(node_name, title=profile.get('headline', ''))
            for other_profile in profiles:
                if other_profile != profile:
                    other_name = f"{other_profile.get('firstName', '')} {other_profile.get('lastName', '')}"
                    G.add_edge(node_name, other_name)

        pos = nx.spring_layout(G)
        edge_trace = [go.Scatter(x=[pos[edge[0]][0], pos[edge[1]][0]], y=[pos[edge[0]][1], pos[edge[1]][1]],
                                 line=dict(width=0.5, color='#888'), hoverinfo='none', mode='lines') for edge in G.edges()]
        node_trace = go.Scatter(x=[pos[node][0] for node in G.nodes()],
                                y=[pos[node][1] for node in G.nodes()],
                                text=[f"{node} ({G.nodes[node]['title']})" for node in G.nodes()],
                                mode='markers+text',
                                marker=dict(size=10, colorbar=dict(thickness=15, title='Conexiones', xanchor='left', titleside='right')))
        fig = go.Figure(data=edge_trace + [node_trace],
                        layout=go.Layout(title='<br>Red de Interacciones entre Perfiles de LinkedIn',
                                         titlefont_size=16, showlegend=False, hovermode='closest',
                                         margin=dict(b=0, l=0, r=0, t=40),
                                         xaxis=dict(showgrid=False, zeroline=False),
                                         yaxis=dict(showgrid=False, zeroline=False)))
        fig.show()
    except Exception as e:
        print(f"Error al visualizar la red de interacciones: {e}")

def visualize_disc(disc_scores, name):
    try:
        labels = list(disc_scores.keys())
        sizes = list(disc_scores.values())
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
        plt.figure(figsize=(8, 6))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title(f'Gráfico DISC de {name}')
        plt.show()
    except Exception as e:
        print(f"Error al visualizar el gráfico DISC: {e}")

if __name__ == "__main__":
    profiles = []
    profile_ids = ['id1', 'id2', 'id3', 'id4', 'id5']  # Lista de IDs de usuarios de LinkedIn

    results = [fetch_linkedin_profile_task.delay(profile_id) for profile_id in profile_ids]

    for result in results:
        profile_data = result.get()
        if profile_data:
            profiles.append(profile_data)

    if profiles:
        df = create_profile_dataframe(profiles)
        print(df)

        visualize_risks(df)
        visualize_network(profiles)

        for profile in profiles:
            name = f"{profile.get('firstName', '')} {profile.get('lastName', '')}"
            disc_scores = calculate_disc(profile)
            visualize_disc(disc_scores, name)
    else:
        print("No se pudieron obtener datos de los perfiles.")
