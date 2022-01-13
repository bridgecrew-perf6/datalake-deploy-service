from database.models import ProjectDB, ProjectCredentialsDB, ProjectDeployDB


class DataLakeDeploymentInterface:
    async def deploy_data_lake(
        self, project: ProjectDB, credentials: ProjectCredentialsDB
    ) -> dict:
        raise NotImplementedError()

    async def delete_data_lake(
        self,
        project: ProjectDB,
        credentials: ProjectCredentialsDB,
        project_deploy: ProjectDeployDB,
    ):
        raise NotImplementedError()