import streamlit as st
import streamlit.components.v1 as components

# 要复制的文本
text_to_copy = "这里是要复制的文本"

# 创建一个按钮，当点击时使用 JavaScript 复制文本
button_html = f"""
<html>
<body>
<input type='text' value='{text_to_copy}' id='text_to_copy' readonly>
<button onclick='myFunction()'>复制文本</button>
<script>
function myFunction() {{
  var copyText = document.getElementById("text_to_copy");
  copyText.select();
  copyText.setSelectionRange(0, 99999); /* For mobile devices */
  navigator.clipboard.writeText(copyText.value);
}}
</script>
</body>
</html>
"""

# 使用 Streamlit components 显示按钮
components.html(button_html, height=100)
