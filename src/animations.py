
"""
Animation Components for JARVIS Interface
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time
from typing import Dict, Any

class JarvisAnimations:
    """JARVIS themed animations and visual effects"""
    
    def __init__(self):
        self.colors = {
            'primary': '#00ffff',
            'secondary': '#ff6b35',
            'accent': '#ffd700',
            'success': '#00ff41',
            'error': '#ff5722'
        }
    
    def create_wave_animation(self) -> go.Figure:
        """Create animated wave pattern for background"""
        x = np.linspace(0, 4*np.pi, 100)
        y1 = np.sin(x) * 0.5
        y2 = np.sin(x + np.pi/4) * 0.3
        y3 = np.sin(x + np.pi/2) * 0.7
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=x, y=y1,
            mode='lines',
            line=dict(color=self.colors['primary'], width=2),
            name='Wave 1'
        ))
        
        fig.add_trace(go.Scatter(
            x=x, y=y2,
            mode='lines',
            line=dict(color=self.colors['secondary'], width=2),
            name='Wave 2'
        ))
        
        fig.add_trace(go.Scatter(
            x=x, y=y3,
            mode='lines',
            line=dict(color=self.colors['accent'], width=2),
            name='Wave 3'
        ))
        
        fig.update_layout(
            showlegend=False,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            height=200
        )
        
        return fig
    
    def create_neural_network_viz(self, activity: float = 0.5) -> go.Figure:
        """Create neural network visualization"""
        # Create nodes
        nodes_x = []
        nodes_y = []
        node_colors = []
        
        # Input layer
        for i in range(4):
            nodes_x.append(0)
            nodes_y.append(i)
            node_colors.append(self.colors['primary'])
        
        # Hidden layer
        for i in range(6):
            nodes_x.append(2)
            nodes_y.append(i - 0.5)
            node_colors.append(self.colors['secondary'])
        
        # Output layer
        for i in range(3):
            nodes_x.append(4)
            nodes_y.append(i + 0.5)
            node_colors.append(self.colors['accent'])
        
        fig = go.Figure()
        
        # Add connections
        for i in range(4):  # Input to hidden
            for j in range(6):
                fig.add_trace(go.Scatter(
                    x=[0, 2], y=[i, j-0.5],
                    mode='lines',
                    line=dict(color='rgba(255,255,255,0.2)', width=1),
                    showlegend=False
                ))
        
        for i in range(6):  # Hidden to output
            for j in range(3):
                fig.add_trace(go.Scatter(
                    x=[2, 4], y=[i-0.5, j+0.5],
                    mode='lines',
                    line=dict(color='rgba(255,255,255,0.2)', width=1),
                    showlegend=False
                ))
        
        # Add nodes
        fig.add_trace(go.Scatter(
            x=nodes_x, y=nodes_y,
            mode='markers',
            marker=dict(
                size=[15 + 5*activity for _ in nodes_x],
                color=node_colors,
                opacity=0.7 + 0.3*activity,
                line=dict(width=2, color='white')
            ),
            showlegend=False
        ))
        
        fig.update_layout(
            showlegend=False,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            height=300
        )
        
        return fig
    
    def create_system_monitor(self, cpu_usage: float, memory_usage: float, network_activity: float) -> go.Figure:
        """Create system monitoring dashboard"""
        fig = go.Figure()
        
        # CPU Usage
        fig.add_trace(go.Scatter(
            x=list(range(20)),
            y=[cpu_usage + np.random.normal(0, 5) for _ in range(20)],
            mode='lines+markers',
            name='CPU Usage',
            line=dict(color=self.colors['primary'], width=3)
        ))
        
        # Memory Usage
        fig.add_trace(go.Scatter(
            x=list(range(20)),
            y=[memory_usage + np.random.normal(0, 3) for _ in range(20)],
            mode='lines+markers',
            name='Memory Usage',
            line=dict(color=self.colors['secondary'], width=3)
        ))
        
        # Network Activity
        fig.add_trace(go.Scatter(
            x=list(range(20)),
            y=[network_activity + np.random.normal(0, 10) for _ in range(20)],
            mode='lines+markers',
            name='Network Activity',
            line=dict(color=self.colors['accent'], width=3)
        ))
        
        fig.update_layout(
            title="System Performance",
            xaxis_title="Time",
            yaxis_title="Usage %",
            plot_bgcolor='rgba(10,10,10,0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    
    def render_matrix_rain(self) -> None:
        """Render Matrix-style falling code effect"""
        st.markdown("""
        <div id="matrix-container" style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
            overflow: hidden;
        ">
            <canvas id="matrix-canvas"></canvas>
        </div>
        
        <script>
        const canvas = document.getElementById('matrix-canvas');
        const ctx = canvas.getContext('2d');
        
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        
        const matrix = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789@#$%^&*()*&^%+-/~{[|`]}";
        const matrixArray = matrix.split("");
        
        const fontSize = 10;
        const columns = canvas.width / fontSize;
        
        const drops = [];
        for(let x = 0; x < columns; x++) {
            drops[x] = 1;
        }
        
        function draw() {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.04)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.fillStyle = '#00ffff';
            ctx.font = fontSize + 'px monospace';
            
            for(let i = 0; i < drops.length; i++) {
                const text = matrixArray[Math.floor(Math.random() * matrixArray.length)];
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                
                if(drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                drops[i]++;
            }
        }
        
        setInterval(draw, 35);
        
        window.addEventListener('resize', function() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        });
        </script>
        """, unsafe_allow_html=True)

    def create_hologram_effect(self, text: str) -> None:
        """Create holographic text effect"""
        st.markdown(f"""
        <div style="
            text-align: center;
            font-family: 'Orbitron', monospace;
            font-size: 2.5rem;
            font-weight: 700;
            color: #00ffff;
            text-shadow: 
                0 0 5px #00ffff,
                0 0 10px #00ffff,
                0 0 15px #00ffff,
                0 0 20px #00ffff;
            animation: hologram 3s infinite;
            margin: 20px 0;
        ">
            {text}
        </div>
        
        <style>
        @keyframes hologram {{
            0%, 100% {{ 
                opacity: 1; 
                transform: scale(1);
            }}
            50% {{ 
                opacity: 0.8; 
                transform: scale(1.02);
            }}
        }}
        </style>
        """, unsafe_allow_html=True)
