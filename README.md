# Overview



## Install

{% tabs %}
{% tab title="Python" %}
```bash
pip install --upgrade spx
```
{% endtab %}
{% endtabs %}

## Configure

{% tabs %}
{% tab title="Python" %}
```python
import spx
spx.init(
    host="ORGANIZATION.simplephysx.io/PROJECT_NAME/SERVER_NAME",
    port=PORT_NO,
    key=KEY
)   
```
{% endtab %}
{% endtabs %}



## Verify



{% tabs %}
{% tab title="Python" %}
```python
print(spx.status())
```
{% endtab %}
{% endtabs %}
