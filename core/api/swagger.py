import coreapi
import coreschema
from rest_framework import response
from rest_framework.decorators import renderer_classes, api_view
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer


@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    schema = coreapi.Document(
        title='Occurrence Search API',
        content={
            'create': coreapi.Link(
                url='/api/occurrence/',
                action='get',
                fields=[
                    coreapi.Field(
                        name='urls',
                        required=True,
                        schema=coreschema.Array(),
                        description='Lista de sites iniciado com http ou https.'
                    ),
                    coreapi.Field(
                        name='word',
                        required=True,
                        description='Palavra buscada.'
                    ),
                ],
                description='Count specific word occurrence on pages.'
            )
        }
    )
    # schema = generator.get_schema(request)
    return response.Response(schema)
