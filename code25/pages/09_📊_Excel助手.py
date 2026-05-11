"""Excel / CSV 数据助手 —— 表格展示与可视化图表"""
import os
import streamlit as st
import pandas as pd
from utils.ui_helpers import apply_custom_css
from config.settings import ALLOWED_DOC_EXTENSIONS

apply_custom_css()

# ==================== 侧边栏 ====================
with st.sidebar:
    st.markdown("## 📊 数据助手配置")

    st.markdown("#### 📄 文件设置")
    encoding_options = ["utf-8", "gbk", "gb2312", "utf-16", "latin-1"]
    file_encoding = st.selectbox("文件编码", encoding_options, key="excel_encoding")

    st.markdown("#### 📈 图表设置")
    chart_theme = st.selectbox("配色主题", ["默认", "柔和", "鲜艳", "深色"], key="chart_theme")

    st.markdown("---")
    st.markdown("#### 💡 使用提示")
    st.caption("- 支持 CSV/XLSX 格式")
    st.caption("- 文件建议小于 20MB")
    st.caption("- 大文件会自动取前 10000 行展示")
    st.caption("- 支持数据筛选和排序")

# ==================== 主区域 ====================
st.title("📊 Excel / CSV 数据助手")
st.caption("上传表格文件，自动展示数据并生成可视化图表")

# 文件上传
uploaded_file = st.file_uploader(
    "📄 上传 CSV 或 Excel 文件",
    type=["csv", "xlsx", "xls"],
    key="excel_upload",
    label_visibility="collapsed"
)

if not uploaded_file:
    # 显示引导
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="text-align:center; padding:30px; background:#f8faff; border-radius:12px; border:1px solid #e0e0e0;">
            <div style="font-size:40px;">📄</div>
            <div style="font-weight:600; margin:8px 0;">上传文件</div>
            <div style="color:#757575; font-size:13px;">支持 CSV / XLSX 格式</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="text-align:center; padding:30px; background:#f8faff; border-radius:12px; border:1px solid #e0e0e0;">
            <div style="font-size:40px;">🔍</div>
            <div style="font-weight:600; margin:8px 0;">数据预览</div>
            <div style="color:#757575; font-size:13px;">自动解析列名和数据类型</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="text-align:center; padding:30px; background:#f8faff; border-radius:12px; border:1px solid #e0e0e0;">
            <div style="font-size:40px;">📊</div>
            <div style="font-weight:600; margin:8px 0;">可视化图表</div>
            <div style="color:#757575; font-size:13px;">折线图、柱状图、饼图等</div>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# ==================== 数据加载 ====================
try:
    file_ext = os.path.splitext(uploaded_file.name)[1].lower()
    if file_ext == ".csv":
        df = pd.read_csv(uploaded_file, encoding=file_encoding, nrows=10000)
    elif file_ext in [".xlsx", ".xls"]:
        df = pd.read_excel(uploaded_file, nrows=10000)
    else:
        st.error("不支持的文件格式")
        st.stop()
except UnicodeDecodeError:
    st.error(f"文件编码不匹配，请在侧边栏切换编码格式（当前: {file_encoding}）")
    st.stop()
except Exception as e:
    st.error(f"文件读取失败: {str(e)}")
    st.stop()

if df.empty:
    st.warning("文件内容为空")
    st.stop()

# ==================== 数据概览 ====================
st.markdown("---")
st.markdown("### 📋 数据概览")

col_info1, col_info2, col_info3, col_info4 = st.columns(4)
with col_info1:
    st.metric("总行数", f"{len(df):,}")
with col_info2:
    st.metric("总列数", len(df.columns))
with col_info3:
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    st.metric("数值列", len(numeric_cols))
with col_info4:
    missing = df.isnull().sum().sum()
    st.metric("缺失值", f"{missing:,}")

# 数据类型信息
with st.expander("📊 列信息详情", expanded=False):
    col_info = pd.DataFrame({
        "列名": df.columns,
        "数据类型": df.dtypes.values,
        "非空数量": df.count().values,
        "缺失数量": df.isnull().sum().values,
        "唯一值": df.nunique().values,
    })
    st.dataframe(col_info, use_container_width=True, hide_index=True)

# ==================== 数据筛选 ====================
st.markdown("### 🔍 数据筛选")

filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    # 列选择
    selected_columns = st.multiselect(
        "选择显示的列",
        df.columns.tolist(),
        default=df.columns.tolist(),
        key="select_cols"
    )

with filter_col2:
    # 行数限制
    max_rows = st.slider("显示行数", 10, min(len(df), 10000), min(100, len(df)), 10, key="max_rows")

# 应用筛选
if selected_columns:
    df_display = df[selected_columns].head(max_rows)
else:
    df_display = df.head(max_rows)

# 排序
if numeric_cols:
    sort_col = st.selectbox("按列排序（可选）", ["不排序"] + numeric_cols, key="sort_col")
    if sort_col != "不排序":
        sort_order = st.radio("排序方式", ["升序", "降序"], horizontal=True, key="sort_order")
        df_display = df_display.sort_values(
            by=sort_col,
            ascending=(sort_order == "升序")
        )

# ==================== 数据表格 ====================
st.markdown("### 📄 数据表格")
st.dataframe(df_display, use_container_width=True, height=400, hide_index=True)

# 下载按钮
csv_export = df_display.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    "⬇ 导出筛选后的数据 (CSV)",
    csv_export,
    f"filtered_{uploaded_file.name}",
    "text/csv",
    use_container_width=True
)

# ==================== 可视化图表 ====================
st.markdown("---")
st.markdown("### 📈 可视化图表")

if not numeric_cols:
    st.info("当前数据没有数值列，无法生成图表。请上传包含数值数据的文件。")
    st.stop()

# 图表主题配色
theme_colors = {
    "默认": ["#1E88E5", "#4CAF50", "#FF9800", "#F44336", "#9C27B0", "#00BCD4", "#FF5722", "#607D8B"],
    "柔和": ["#81D4FA", "#A5D6A7", "#FFE082", "#EF9A90", "#CE93D8", "#80DEEA", "#FFAB91", "#B0BEC5"],
    "鲜艳": ["#2196F3", "#4CAF50", "#FFC107", "#FF5722", "#9C27B0", "#00BCD4", "#E91E63", "#3F51B5"],
    "深色": ["#0D47A1", "#1B5E20", "#E65100", "#B71C1C", "#4A148C", "#006064", "#BF360C", "#263238"],
}
colors = theme_colors.get(chart_theme, theme_colors["默认"])

chart_type = st.selectbox(
    "选择图表类型",
    ["折线图", "柱状图", "饼图", "散点图", "面积图"],
    key="chart_type"
)

# 数据列选择
all_cols = df.columns.tolist()

if chart_type == "饼图":
    # 饼图需要分类列和数值列
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    if not cat_cols:
        st.warning("饼图需要至少一个文本/分类列作为标签")
    else:
        pie_cat_col = st.selectbox("标签列（分类）", cat_cols, key="pie_cat")
        pie_val_col = st.selectbox("数值列", numeric_cols, key="pie_val")

        # 聚合数据（取前 10 个类别）
        pie_data = df.groupby(pie_cat_col)[pie_val_col].sum().nlargest(10).reset_index()

        st.markdown(f"#### 🥧 {pie_val_col} - 按 {pie_cat_col} 分布")
        st.plotly_chart(
            {
                "data": [{
                    "type": "pie",
                    "labels": pie_data[pie_cat_col].tolist(),
                    "values": pie_data[pie_val_col].tolist(),
                    "marker": {"colors": colors},
                    "textinfo": "label+percent",
                    "hole": 0.3,
                }],
                "layout": {
                    "height": 450,
                    "margin": {"t": 20, "b": 20, "l": 20, "r": 20},
                }
            },
            use_container_width=True
        )

else:
    # 折线图/柱状图/散点图/面积图
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        x_col = st.selectbox("X 轴", all_cols, key="chart_x")
    with chart_col2:
        y_cols = st.multiselect("Y 轴（可多选）", numeric_cols, default=[numeric_cols[0]] if numeric_cols else [], key="chart_y")

    if not y_cols:
        st.info("请选择至少一个 Y 轴数值列")
    else:
        # 去掉 x 轴中的 NaN 并排序
        df_chart = df[[x_col] + y_cols].dropna(subset=[x_col]).head(500)

        chart_type_map = {
            "折线图": "scatter",
            "柱状图": "bar",
            "散点图": "scatter",
            "面积图": "scatter",
        }
        plotly_type = chart_type_map[chart_type]

        traces = []
        for i, y_col in enumerate(y_cols):
            trace = {
                "type": plotly_type,
                "x": df_chart[x_col].tolist(),
                "y": df_chart[y_col].tolist(),
                "name": y_col,
                "line": {"color": colors[i % len(colors)], "width": 2} if plotly_type == "scatter" else None,
                "marker": {"color": colors[i % len(colors)]} if plotly_type == "bar" else None,
            }
            if chart_type == "散点图":
                trace["mode"] = "markers"
                trace["marker"] = {"color": colors[i % len(colors)], "size": 6, "opacity": 0.7}
            elif chart_type == "折线图":
                trace["mode"] = "lines+markers"
                trace["fill"] = "none"
            elif chart_type == "面积图":
                trace["mode"] = "lines"
                trace["fill"] = "tozeroy"
                trace["fillcolor"] = colors[i % len(colors)] + "30"
            traces.append(trace)

        layout = {
            "height": 450,
            "margin": {"t": 30, "b": 50, "l": 60, "r": 20},
            "xaxis": {"title": x_col, "tickangle": -45 if len(df_chart) > 20 else 0},
            "yaxis": {"title": " / ".join(y_cols)},
            "legend": {"orientation": "h", "y": 1.12},
            "hovermode": "x unified",
        }

        st.plotly_chart({"data": traces, "layout": layout}, use_container_width=True)

# ==================== 数据统计 ====================
st.markdown("---")
st.markdown("### 📊 数据统计")

if numeric_cols:
    st.dataframe(df[numeric_cols].describe().round(2), use_container_width=True)

    # 相关性矩阵
    if len(numeric_cols) >= 2:
        with st.expander("🔗 相关性分析", expanded=False):
            corr = df[numeric_cols].corr().round(2)
            st.dataframe(corr, use_container_width=True)

            # 热力图
            heatmap_data = [{
                "type": "heatmap",
                "x": numeric_cols,
                "y": numeric_cols,
                "z": corr.values.tolist(),
                "colorscale": "RdBu_r",
                "zmin": -1,
                "zmax": 1,
                "text": corr.values.round(2).tolist(),
                "texttemplate": "%{text}",
                "hoverinfo": "z",
            }]
            heatmap_layout = {
                "height": 400,
                "margin": {"t": 20, "b": 80, "l": 100, "r": 20},
                "xaxis": {"tickangle": -45},
            }
            st.plotly_chart({"data": heatmap_data, "layout": heatmap_layout}, use_container_width=True)
else:
    st.info("当前数据没有数值列，无法生成统计信息。")
