import streamlit_antd_components as sac

sac.cascader(items=[
    # sac.CasItem('home'),
    # sac.CasItem('other1'),
    # sac.CasItem('other2')
], label='label', index=0, format_func='title', multiple=False, search=True, clear=True)