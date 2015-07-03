## pyalfresco

Scripts for interacting with alfresco from python.

# Example:

    from pyalfresco import Alfresco

    alf = Alfresco("alfresco.corp.com", "username", "password")
    alf.basic_authentication()
    alf.initiate_bulk_import({
            "sourceDirectory": "/mydocuments",
            "contentStore": "default",
            "targetPath": "/Company Home/online_documents"
    })
