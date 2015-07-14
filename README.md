# pyalfresco

Scripts for interacting with the Document Management System [Alfresco](http://www.alfresco.com) from python.

## Bulk Import

```python
from pyalfresco import Alfresco

alf = Alfresco("alfresco.corp.com", "username", "password")
alf.basic_authentication()
alf.initiate_bulk_import({
        "sourceDirectory": "/mydocuments",
        "contentStore": "default",
        "targetPath": "/Company Home/online_documents"
})
```

## Webscripts

```python
from pyalfresco import Alfresco

alf = Alfresco("alfresco.corp.com", "username", "password")
alf.ticket_authentication()
response = alf.call_webscript("/your/webscript/path")
```
