import streamlit as st
import pandas as pd
import plotly.express as px
import networkx as nx
import plotly.graph_objects as go
from io import StringIO

def main():
    st.title("Interactive Data Visualization Dashboard")
    
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"]) 
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Dataset Preview:")
        st.write(df.head())
        
        chart_type = st.selectbox("Select chart type", [
            "Radial Bar Chart", "Radar Chart", "Nightingale Chart", "Donut Chart", "Treemap Chart", "Sunburst Chart", "Chord Diagram", "Network Diagram"
        ])
        
        if chart_type in ["Radial Bar Chart", "Radar Chart", "Nightingale Chart", "Donut Chart"]:
            numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
            category_column = st.selectbox("Select categorical column", df.columns)
            value_column = st.selectbox("Select numerical column", numeric_columns)
            
            if chart_type == "Radial Bar Chart":
                fig = px.bar_polar(df, r=value_column, theta=category_column, color=category_column, template="plotly_dark")
            elif chart_type == "Radar Chart":
                fig = px.line_polar(df, r=value_column, theta=category_column, line_close=True, template="plotly_dark")
            elif chart_type == "Nightingale Chart":
                fig = px.bar_polar(df, r=value_column, theta=category_column, color=category_column, template="plotly_dark")
            elif chart_type == "Donut Chart":
                fig = px.pie(df, names=category_column, values=value_column, hole=0.4, template="plotly_dark")
                
        elif chart_type == "Treemap Chart":
            category_column = st.selectbox("Select categorical column", df.columns)
            value_column = st.selectbox("Select numerical column", df.select_dtypes(include=['number']).columns.tolist())
            fig = px.treemap(df, path=[category_column], values=value_column, color=value_column, template="plotly_dark")
            
        elif chart_type == "Sunburst Chart":
            category_column = st.selectbox("Select categorical column", df.columns)
            value_column = st.selectbox("Select numerical column", df.select_dtypes(include=['number']).columns.tolist())
            fig = px.sunburst(df, path=[category_column], values=value_column, color=value_column, template="plotly_dark")
            
        elif chart_type == "Chord Diagram":
            st.warning("Ensure your dataset contains a 'source', 'target', and 'value' column.")
            if all(col in df.columns for col in ["source", "target", "value"]):
                fig = go.Figure()
                for _, row in df.iterrows():
                    fig.add_trace(go.Scatter(x=[row["source"], row["target"]], y=[1, 1], mode='lines', line=dict(width=row["value"])))
                fig.update_layout(title="Chord Diagram", template="plotly_dark")
            else:
                st.error("Dataset must contain 'source', 'target', and 'value' columns.")
                return
            
        elif chart_type == "Network Diagram":
            st.warning("Ensure your dataset contains a 'source' and 'target' column.")
            if all(col in df.columns for col in ["source", "target"]):
                G = nx.from_pandas_edgelist(df, source="source", target="target")
                pos = nx.spring_layout(G)
                edge_x = []
                edge_y = []
                for edge in G.edges():
                    x0, y0 = pos[edge[0]]
                    x1, y1 = pos[edge[1]]
                    edge_x.append(x0)
                    edge_x.append(x1)
                    edge_x.append(None)
                    edge_y.append(y0)
                    edge_y.append(y1)
                    edge_y.append(None)
                
                edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=1), hoverinfo='none', mode='lines')
                node_x = []
                node_y = []
                for node in G.nodes():
                    x, y = pos[node]
                    node_x.append(x)
                    node_y.append(y)
                
                node_trace = go.Scatter(x=node_x, y=node_y, mode='markers', hoverinfo='text', marker=dict(size=10))
                
                fig = go.Figure(data=[edge_trace, node_trace])
                fig.update_layout(title="Network Diagram", showlegend=False, template="plotly_dark")
            else:
                st.error("Dataset must contain 'source' and 'target' columns.")
                return
        
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()