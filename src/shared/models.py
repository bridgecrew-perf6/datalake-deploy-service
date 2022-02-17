import inspect
import typing
from enum import Enum

from pydantic import UUID4, BaseModel, constr, stricturl


def optional(*fields):
    """Decorator function used to modify a pydantic model's fields to all be optional.
    Alternatively, you can  also pass the field names that should be made optional as
    arguments to the decorator.
    Taken from https://github.com/samuelcolvin/pydantic/issues/1223#issuecomment-775363074
    """

    def dec(_cls):
        for field in fields:
            _cls.__fields__[field].required = False
        return _cls

    if fields and inspect.isclass(fields[0]) and issubclass(fields[0], BaseModel):
        cls = fields[0]
        fields = cls.__fields__
        return dec(cls)

    return dec


class ServiceProviderType(str, Enum):
    AWS = "AWS"
    AZURE = "AZURE"
    GCP = "GCP"


class ProjectMixin(BaseModel):
    verified: typing.Optional[bool] = False
    name: str
    service_provider: constr(
        regex=rf"^({'|'.join([e.value for e in ServiceProviderType])})$"  # noqa
    )

    def create_update_dict(self):
        return self.dict(
            exclude_unset=True,
            exclude={
                "id",
                "verified",
            },
        )

    def create_update_dict_superuser(self):
        return self.dict(exclude_unset=True, exclude={"id"})


class GCPCredentials(BaseModel):
    type: constr(max_length=256)
    project_id: constr(max_length=256)
    private_key_id: constr(min_length=40, max_length=40)
    private_key: constr(max_length=2096)
    client_email: constr(max_length=256)
    client_id: constr(min_length=21, max_length=21, regex=r"^\d+$")  # noqa
    auth_uri: stricturl(max_length=256)
    token_uri: stricturl(max_length=256)
    auth_provider_x509_cert_url: stricturl(max_length=256)
    client_x509_cert_url: stricturl(max_length=256)


class AWSCredentials(BaseModel):
    access_key_id: constr(max_length=256)
    secret_access_key: constr(max_length=256)


class AzureCredentials(BaseModel):
    tenant_id: constr(max_length=256)
    client_id: constr(max_length=100)
    client_secret: constr(max_length=100)


class ProjectCredentialsMixin(BaseModel):
    project: typing.Optional[UUID4]
    credentials: typing.Union[GCPCredentials, AWSCredentials, AzureCredentials]

    def create_update_dict(self):
        return self.dict(
            exclude_unset=True,
            exclude={
                "id",
                "project",
            },
        )

    def create_update_dict_superuser(self):
        return self.dict(exclude_unset=True, exclude={"id"})


class AWSProjectDeployType(str, Enum):
    AWS_1 = "AWS_1"


class GCPProjectDeployType(str, Enum):
    GCP_1 = "GCP_1"
    GCP_2 = "GCP_2"


class ProjectDeployMixin(BaseModel):
    project: typing.Optional[UUID4]
    deploy_type: constr(
        regex=rf"^({'|'.join([e.value for e in (*AWSProjectDeployType, *GCPProjectDeployType)])})$"  # noqa
    )
    project_structure: typing.Optional[dict]

    def create_update_dict(self):
        return self.dict(
            exclude_unset=True,
            exclude={
                "id",
                "project",
            },
        )

    def create_update_dict_superuser(self):
        return self.dict(exclude_unset=True, exclude={"id"})
