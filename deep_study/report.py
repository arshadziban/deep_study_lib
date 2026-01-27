# report module
"""
Report Generator: Creates HTML reports with feature profiles and correlations.
"""

import os
import base64
from io import BytesIO
import matplotlib
import matplotlib.pyplot as plt
from jinja2 import Environment, FileSystemLoader


class Report:
    """
    Report class containing analysis results and export methods.
    
    Parameters
    ----------
    df : pd.DataFrame
        Encoded DataFrame
    raw_df : pd.DataFrame
        Original DataFrame (before encoding)
    correlations : dict
        Feature correlation scores with target
    importance : dict
        Feature importance scores from ML model
    target : str
        Target type ('numeric' or 'categorical')
    target_name : str
        Name of target column
    feature_profiles : list
        List of feature profile dictionaries
    correlation_summary : list
        List of correlation summaries with target
    """
    
    def __init__(self, df, raw_df, correlations, importance, target, 
                 target_name, feature_profiles, correlation_summary):
        self.df = df
        self.raw_df = raw_df
        self.correlations = correlations
        self.importance = importance
        self.target = target
        self.target_name = target_name
        self.feature_profiles = feature_profiles
        self.correlation_summary = correlation_summary

    def _plot_to_base64(self, fig):
        """Convert matplotlib figure to base64 string."""
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close(fig)
        return f"data:image/png;base64,{img_base64}"

    def _sanitize_text(self, text):
        """Remove or replace problematic characters for matplotlib fonts."""
        if not isinstance(text, str):
            text = str(text)
        # Replace common problematic characters
        replacements = {
            '\x80': '-',  # Euro sign placeholder
            '\x93': '-',  # Em dash
            '\x94': '-',  # Em dash
            '–': '-',     # En dash
            '—': '-',     # Em dash
            ''': "'",     # Smart quote
            ''': "'",     # Smart quote
            '"': '"',     # Smart quote
            '"': '"',     # Smart quote
            '…': '...',   # Ellipsis
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        # Remove any remaining non-ASCII characters that might cause issues
        text = text.encode('ascii', 'replace').decode('ascii')
        return text

    def _plot_bar(self, data, title, color='#3498db', top_n=15):
        """Create horizontal bar chart."""
        fig, ax = plt.subplots(figsize=(8, max(4, len(list(data.keys())[:top_n]) * 0.4)))
        names = [self._sanitize_text(n) for n in list(data.keys())[:top_n][::-1]]
        values = list(data.values())[:top_n][::-1]
        
        bars = ax.barh(names, values, color=color)
        ax.set_title(self._sanitize_text(title), fontsize=12, fontweight='bold')
        ax.set_xlabel('Score')
        
        # Add value labels
        for bar, val in zip(bars, values):
            ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, 
                   f'{val:.4f}', va='center', fontsize=8)
        
        plt.tight_layout()
        return self._plot_to_base64(fig)

    def _format_large_number(self, num):
        """Format large numbers for display."""
        if num is None:
            return "N/A"
        try:
            num = float(num)
            if abs(num) >= 1_000_000_000:
                return f"{num/1_000_000_000:.2f}B"
            elif abs(num) >= 1_000_000:
                return f"{num/1_000_000:.2f}M"
            elif abs(num) >= 1_000:
                return f"{num/1_000:.2f}K"
            elif abs(num) < 1 and num != 0:
                return f"{num:.4f}"
            else:
                return f"{num:,.2f}"
        except:
            return str(num)

    def _plot_feature_distribution(self, profile):
        """Create distribution plot for a feature."""
        # Only create plots for numeric features
        if profile["type"] == "Numeric" and "histogram" in profile:
            fig, ax = plt.subplots(figsize=(5, 3))
            hist = profile["histogram"]
            
            # Limit to 10 bins for cleaner display
            edges = hist["edges"]
            counts = hist["counts"]
            
            # If more than 10 bins, resample to 10
            if len(counts) > 10:
                import numpy as np
                new_counts = []
                new_edges = [edges[0]]
                step = len(counts) // 10
                for i in range(10):
                    start_idx = i * step
                    end_idx = (i + 1) * step if i < 9 else len(counts)
                    new_counts.append(sum(counts[start_idx:end_idx]))
                    new_edges.append(edges[end_idx])
                counts = new_counts
                edges = new_edges
            
            centers = [(edges[i] + edges[i+1])/2 for i in range(len(edges)-1)]
            ax.bar(centers, counts, 
                  width=(edges[1]-edges[0])*0.9,
                  color='#6475C3', alpha=0.8)
            ax.set_xlabel('Value')
            ax.set_ylabel('Count')
            ax.set_title(self._sanitize_text(profile["name"]), fontsize=10, fontweight='bold')
            
            # Format x-axis for large numbers
            ax.ticklabel_format(style='plain', axis='x')
            ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: self._format_large_number(x)))
            plt.xticks(rotation=45, ha='right')
            
            plt.tight_layout()
            return self._plot_to_base64(fig)
        
        # Return None for categorical features (no bar chart)
        return None

    def _render_html(self):
        """Generate HTML content for the report."""
        # Generate correlation plot
        corr_plot = self._plot_bar(
            self.correlations,
            f"Feature Correlation with {self.target_name}",
            color='#2ecc71'
        )
        
        # Generate importance plot
        imp_plot = self._plot_bar(
            self.importance,
            f"Feature Importance (Random Forest)",
            color='#e74c3c'
        )
        
        # Generate distribution plots for each feature
        for profile in self.feature_profiles:
            if "dist_plot" not in profile:
                profile["dist_plot"] = self._plot_feature_distribution(profile)
        
        # Load and render template
        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template("report.html")
        
        return template.render(
            target=self.target_name,
            target_type=self.target,
            rows=self.df.shape[0],
            cols=self.df.shape[1],
            correlations=list(self.correlations.items()),
            corr_plot=corr_plot,
            importance_plot=imp_plot,
            feature_profiles=self.feature_profiles,
            correlation_summary=self.correlation_summary
        )
    
    def _repr_html_(self):
        """Display report inline in Jupyter notebook."""
        html_content = self._render_html()
        # Use iframe with srcdoc to completely isolate styles and force white background
        import html
        escaped_html = html.escape(html_content)
        return f'''<iframe srcdoc="{escaped_html}" style="width: 100%; height: 800px; border: 1px solid #ddd; border-radius: 8px; background-color: #ffffff;"></iframe>'''
    
    def show(self):
        """Display report in Jupyter notebook."""
        from IPython.display import HTML, display
        html_content = self._render_html()
        import html as html_module
        escaped_html = html_module.escape(html_content)
        iframe_html = f'''<iframe srcdoc="{escaped_html}" style="width: 100%; height: 800px; border: 1px solid #ddd; border-radius: 8px; background-color: #ffffff;"></iframe>'''
        display(HTML(iframe_html))
    
    def get_top_features(self, n=10):
        """Get top N correlated features with target."""
        return dict(list(self.correlations.items())[:n])
    
    def get_feature_profile(self, feature_name):
        """Get profile for a specific feature."""
        for profile in self.feature_profiles:
            if profile["name"] == feature_name:
                return profile
        return None
