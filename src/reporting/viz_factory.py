import plotly.graph_objects as go
import plotly.express as px
import os

class SeniorViz:
    """
    Motor de visualização executiva para a Fábrica de Data Science.
    Focado em estética premium, títulos narrativos e clareza de ROI.
    """
    
    COLORS = {
        'primary': '#1A73E8',  # Azul Executivo
        'secondary': '#5F6368', # Cinza Contextual
        'accent': '#E37400',    # Laranja para Destaque/Alerta
        'background': '#FFFFFF',
        'text': '#202124'
    }

    @staticmethod
    def apply_style(fig, title, subtitle=None):
        """Aplica o template visual sênior ao gráfico Plotly."""
        fig.update_layout(
            title={
                'text': f"<b>{title}</b><br><span style='font-size: 14px; color: #5F6368;'>{subtitle if subtitle else ''}</span>",
                'x': 0.05,
                'xanchor': 'left'
            },
            font=dict(family="Arial, sans-serif", size=14, color=SeniorViz.COLORS['text']),
            plot_bgcolor=SeniorViz.COLORS['background'],
            paper_bgcolor=SeniorViz.COLORS['background'],
            margin=dict(t=100, b=50, l=50, r=50),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        return fig

    @staticmethod
    def create_line_chart(df, x, y, title, subtitle=None):
        """Gera um gráfico de linha executivo."""
        fig = px.line(df, x=x, y=y, color_discrete_sequence=[SeniorViz.COLORS['primary']])
        fig.update_traces(line=dict(width=3))
        return SeniorViz.apply_style(fig, title, subtitle)

    @staticmethod
    def create_donut_chart(df, names, values, title, subtitle=None):
        """Gera um gráfico de rosca executivo."""
        fig = go.Figure(data=[go.Pie(
            labels=df[names], 
            values=df[values], 
            hole=.6,
            marker=dict(colors=[SeniorViz.COLORS['primary'], SeniorViz.COLORS['secondary'], SeniorViz.COLORS['accent']])
        )])
        return SeniorViz.apply_style(fig, title, subtitle)

    @staticmethod
    def create_column_chart(df, x, y, title, subtitle=None, orientation='v'):
        """Gera um gráfico de colunas/barras executivo."""
        if orientation == 'v':
            fig = px.bar(df, x=x, y=y, color_discrete_sequence=[SeniorViz.COLORS['primary']])
        else:
            fig = px.bar(df, x=y, y=x, orientation='h', color_discrete_sequence=[SeniorViz.COLORS['primary']])
        
        fig.update_traces(marker_line_width=0)
        return SeniorViz.apply_style(fig, title, subtitle)

    @staticmethod
    def save_chart(fig, project_name, file_name):
        """Salva o gráfico em PNG de alta resolução."""
        path = f"reports/figures/{project_name}"
        if not os.path.exists(path):
            os.makedirs(path)
        
        full_path = f"{path}/{file_name}.png"
        # Usamos engine 'kaleido' para exportação estática
        fig.write_image(full_path, engine="kaleido", scale=2)
        print(f"Grafico salvo em: {full_path}")
