import pytest


@pytest.fixture
def vue_template_with_tailwind_classes():
    return """
    <template>
        <div class="bg-red-200">
            bla
        </div>
        </template>
    """
