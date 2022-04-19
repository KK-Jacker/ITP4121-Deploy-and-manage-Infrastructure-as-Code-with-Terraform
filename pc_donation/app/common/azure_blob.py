import os
from datetime import datetime, timedelta

from azure.storage.blob import generate_container_sas, ContainerSasPermissions, generate_blob_sas, BlobSasPermissions, \
    ContainerClient
from cachetools import cached, TTLCache
from flask import current_app


# save image to blob
# TODO: delete old method
def save_image(blob_name, file_path):
    container_client = ContainerClient.from_connection_string(
        conn_str=current_app.config['AZURE_STORAGE_CONNECTION_STRING'],
        container_name=current_app.config['AZURE_STORAGE_CONTAINER_NAME'])
    with open(file_path, "rb") as data:
        container_blob = container_client.upload_blob(name=blob_name, data=data,
                                                      overwrite=True)
    return container_blob


def upload_image_from_memory(blob_name, data, temp=False):
    if temp is True:
        container_client = ContainerClient.from_connection_string(
            conn_str=current_app.config['AZURE_STORAGE_CONNECTION_STRING'],
            container_name=current_app.config['AZURE_STORAGE_TEMP_CONTAINER_NAME'])
    else:
        container_client = ContainerClient.from_connection_string(
            conn_str=current_app.config['AZURE_STORAGE_CONNECTION_STRING'],
            container_name=current_app.config['AZURE_STORAGE_CONTAINER_NAME'])

    blob = container_client.upload_blob(name=blob_name, data=data,
                                        overwrite=True)
    return blob


# using generate_container_sas
@cached(cache=TTLCache(maxsize=1024, ttl=60 * 50))
def get_img_url_with_container_sas_token(blob_name, temp=False):
    account_name = current_app.config['AZURE_STORAGE_ACCOUNT_NAME']
    account_key = current_app.config['AZURE_STORAGE_ACCOUNT_KEY']
    if temp is True:
        container_name = current_app.config['AZURE_STORAGE_TEMP_CONTAINER_NAME']
    else:
        container_name = current_app.config['AZURE_STORAGE_CONTAINER_NAME']
    container_sas_token = generate_container_sas(
        account_name=account_name,
        container_name=container_name,
        account_key=account_key,
        permission=ContainerSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )
    blob_url_with_container_sas_token = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?" \
                                        f"{container_sas_token}"
    return blob_url_with_container_sas_token


# using generate_blob_sas
@cached(cache=TTLCache(maxsize=1024, ttl=60 * 50))
def get_img_url_with_blob_sas_token(blob_name, temp=False):
    if blob_name is None:
        return None
    if temp is True:
        container_name = current_app.config['AZURE_STORAGE_TEMP_CONTAINER_NAME']
    else:
        container_name = current_app.config['AZURE_STORAGE_CONTAINER_NAME']
    account_name = current_app.config['AZURE_STORAGE_ACCOUNT_NAME']
    account_key = current_app.config['AZURE_STORAGE_ACCOUNT_KEY']
    blob_sas_token = generate_blob_sas(
        account_name=account_name,
        container_name=container_name,
        blob_name=blob_name,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )
    blob_url_with_blob_sas_token = f"https://{account_name}.blob.core.windows.net/{container_name}/" \
                                   f"{blob_name}?{blob_sas_token}"
    return blob_url_with_blob_sas_token


# TODO: delete old method
def upload_user_to_azure_blob(form, photo, field_name="photo"):
    form[field_name].data.save(
        os.path.abspath('app/static/user/' + photo))
    # upload local file to blob
    save_image(blob_name="user/" + photo,
               file_path=os.path.abspath('app/static/user/' +
                                         photo))
    # remove local file
    os.remove(os.path.abspath('app/static/user/' + photo))
    # photo_path = os.path.abspath('app/static/storage/pictures/image/' + volunteer_photo)
    photo_path = get_img_url_with_blob_sas_token(
        "user/" + photo)
    return photo_path
