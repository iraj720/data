import logging

from dependency_injector.wiring import inject, Provide
from flask import Blueprint
from flask import request

from src.api.middleware import post_data_required
from src.api.responses import create_response
from src.api.schemas import (ServiceContextSchema,SearchRequest)
from src.dependency_container import DependencyContainer
from src.api.requests import normalize_query

logger = logging.getLogger(__name__)
blueprint = Blueprint('service_context', __name__)


@blueprint.route('/tag', methods=['POST'])
@post_data_required
@inject
def update_service_context(
    json_data,
    service_context_service=Provide[
        DependencyContainer.service_context_service
    ]
):
    validated_data = ServiceContextSchema().load(json_data)
    service_context = service_context_service.update(validated_data)
    return create_response(service_context, ServiceContextSchema)


@blueprint.route('/search', methods=['POST'])
@post_data_required
@inject
def get_service_status(
    json_data,
    service_context_service=Provide[
        DependencyContainer.service_context_service
    ]
):
    validated_data = SearchRequest().load(json_data)
    status = service_context_service.get(validated_data["index"], validated_data)
    return create_response(status, ServiceContextSchema)
