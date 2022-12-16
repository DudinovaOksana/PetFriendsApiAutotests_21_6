from datetime import datetime

import pytest

from api_for_test_with_fixtures import PetFriendsDecorator
from settings_with_fixtures import invalid_email
from settings_with_fixtures import valid_email
from settings_with_fixtures import valid_password

pf = PetFriendsDecorator()

@pytest.fixture()
def fixture_get_api_key():
    _, res = pf.get_api_key(valid_email, valid_password)
    print("API key: ", res)
    return res


@pytest.fixture()
def fixture_get_api_key_with_invalid_data():
    return 'Invalid_user'


@pytest.fixture(autouse=True)
def time_delta():
    start_time = datetime.now()
    yield
    end_time = datetime.now()
    print(f"\nТест шел: {end_time - start_time}")


#проверяем можно ли получить корректный список питомцев
@pytest.mark.positive_tests
@pytest.mark.debug
def test_get_all_pets_with_valid_data_with_fixture(fixture_get_api_key):
    status, result = pf.get_list_of_pets(fixture_get_api_key, "")
    assert status == 200
    assert len(result['pets']) > 0


#проверяем можно ли корректно создать питомца без фото
@pytest.mark.tests_with_photo
@pytest.mark.positive_tests
def test_create_pet_without_photo_with_fixtures(fixture_get_api_key):
    age = "1"
    name = "Maxim"
    type = "python"
    status, result = pf.add_new_pet_simple_without_photo(fixture_get_api_key, name, type, age)
    assert status == 200
    assert result['age'] == age
    assert result['name'] == name
    assert result['animal_type'] == type


#проверяем можно ли корректно добавить фото питомца
@pytest.mark.tests_with_photo
@pytest.mark.tests_with_photo
def test_add_pet_photo_with_fixture(fixture_get_api_key):
    age = "4"
    name = "Ярослав"
    animal_type = "змея"
    pet_photo = "D:\PycharmProjects\PetFriendsApiAutotests\images\pyt.jpg"
    status, result, head = pf.add_new_pet_with_photo(fixture_get_api_key, name, animal_type, age, pet_photo=pet_photo)
    new_status, new_result = pf.set_pet_photo(fixture_get_api_key, result["id"], pet_photo)
    assert new_status == 200


#проверяем можно ли корректно создать питомца с фото
@pytest.mark.tests_with_photo
@pytest.mark.positive_tests
def test_create_pet_with_photo_with_fixture(fixture_get_api_key):
    age = "1"
    name = "Anton"
    type = "python"
    photo = "D:\PycharmProjects\PetFriendsApiAutotests\images\8077750.png"
    status, result, response_head = pf.add_new_pet_with_photo(fixture_get_api_key, name, type, age, photo)
    assert status == 200
    assert result['age'] == age
    assert result['name'] == name
    assert result['animal_type'] == type
    assert "data:image/jpeg;base64" in result['pet_photo']


#проверяем можно ли корректно обновить сведения о питомце
@pytest.mark.positive_tests
def test_successful_update_pet_info_with_fixture(fixture_get_api_key):
    age = "4"
    name = "Matrisskin"
    animal_type = "Cat"
    _, my_pets = pf.get_list_of_pets(fixture_get_api_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result, _ = pf.change_pet(fixture_get_api_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception('There is no my pets')


# проверяем можно ли корректно удалить животное
@pytest.mark.positive_tests
def test_successful_delete_pet_with_fixture(fixture_get_api_key):
    age = "1"
    name = "Yura_1"
    type = "python"
    photo = "D:\PycharmProjects\PetFriendsApiAutotests\images\8077750.png"
    status, result, response_head = pf.add_new_pet_with_photo(fixture_get_api_key, name, type, age, photo)
    status_delete, result_delete, response_head = pf.delete_pet(fixture_get_api_key, result["id"])
    assert status_delete == 200


# проверяем выдаст ли система ошибку при запросе ключей api с некорректным эл.ящиком
@pytest.mark.xfail(reason="тест только без фикстуры успешен")
@pytest.mark.positive_tests
def test_get_api_key_for_invalid_user_with_fixture():
    status, result = pf.get_api_key(invalid_email,valid_password)
    assert status == 403


# проверяем выдаст ли система ошибку при создании животного без фото без поля "animal_type"
@pytest.mark.positive_tests
def test_create_pet_without_photo_without_animal_type_field_with_fixture(fixture_get_api_key):
    age = '2'
    name = "Mark"
    status, result = pf.add_new_pet_simple_without_photo_without_animal_type_field(fixture_get_api_key, name, age)
    assert status == 400


# проверяем выдаст ли система ошибку при создании животного без фото при отсутствии с некорректным auth-key
@pytest.mark.invalid_key
@pytest.mark.positive_tests
def test_create_pet_without_photo_with_invalid_auth_key_with_fixture(fixture_get_api_key_with_invalid_data):
    age = "2"
    name = "Mark"
    animal_type = "Медведь"
    status, result = pf.add_new_pet_simple_without_photo(fixture_get_api_key_with_invalid_data, name=name, animal_type=animal_type, age=age)
    assert status == 403


# проверяем можно ли создать питомца с фото, где вместо фото загружен текстовый файл
@pytest.mark.tests_with_photo
@pytest.mark.positive_tests
@pytest.mark.xfail(reason="Баг в системе", raises=AssertionError)
def test_create_pet_with_invalid_photo(fixture_get_api_key):
    age = "3"
    name = "Michelle"
    type = "cat"
    pet_photo = "D:\\PycharmProjects\\PetFriendsApiAutotests\\images\\photo.txt"
    status, result, response_head = pf.add_new_pet_with_photo(fixture_get_api_key, name, type, age, pet_photo)
    assert status == 400


# проверяем можно создать питомца с фото с некорректным auth_key
@pytest.mark.tests_with_photo
@pytest.mark.invalid_key
@pytest.mark.positive_tests
def test_create_pet_with_photo_with_invalid_auth_key_with_fixture(fixture_get_api_key_with_invalid_data):
    age = "2"
    name = "John"
    type = "cobra"
    photo = "D:\PycharmProjects\PetFriendsApiAutotests\images\8077750.png"
    status, result, response_head = pf.add_new_pet_with_photo(fixture_get_api_key_with_invalid_data, name=name,
                                                              animal_type=type, age=age, pet_photo=photo)
    assert status == 403


# проверяем можно ли добавить фото питомца с некорректным auth-key
@pytest.mark.invalid_key
@pytest.mark.negative_tests
@pytest.mark.tests_with_photo
@pytest.mark.skip(reason='Баг в системе')
def test_add_pet_photo_invalid_auth_key_with_fixture(fixture_get_api_key_with_invalid_data, fixture_get_api_key):
    age = "3"
    name = "Yan"
    type = "snake"
    status, result = pf.add_new_pet_simple_without_photo(fixture_get_api_key, name, type, age)
    pet_photo = "D:\\PycharmProjects\\PetFriendsApiAutotests\\images\\1575050853qqw.gif"
    status, result = pf.set_pet_photo(fixture_get_api_key_with_invalid_data, pet_id=result["id"], pet_photo=pet_photo)
    assert status == 403


# проверяем можно ли получить список питомцев с некорректным ключом
@pytest.mark.invalid_key
@pytest.mark.positive_tests
@pytest.mark.invalid_key
def test_get_all_pets_with_invalid_key_with_fixture(fixture_get_api_key_with_invalid_data):
    status, result = pf.get_list_of_pets(fixture_get_api_key_with_invalid_data, filter="")
    assert status == 403


# проверяем можно ли удалить питомца с некорректным auth_key
@pytest.mark.invalid_key
@pytest.mark.tests_with_photo
@pytest.mark.positive_tests
def test_delete_pet_with_invalid_auth_key_with_fixture(fixture_get_api_key_with_invalid_data, fixture_get_api_key):
    age = "2"
    name = "Yura_2"
    type = "python"
    photo = "D:\PycharmProjects\PetFriendsApiAutotests\images\8077750.png"
    status, result, response_head = pf.add_new_pet_with_photo(fixture_get_api_key, name, type, age, photo)
    new_status, new_result, new_response_head = pf.delete_pet(fixture_get_api_key_with_invalid_data,
                                                              pet_id=result["id"])
    assert new_status == 403


# проверяем можно ли обновить сведения о питомце с некорректными данными
@pytest.mark.positive_tests
def test_update_pet_info_with_invalid_data_with_fixture(fixture_get_api_key):
    age = "5"
    name = "Kirill"
    animal_type = "Elefant"
    status, result, response_head = pf.change_pet(fixture_get_api_key, "ID_DOESN'T_EXIST", name, animal_type, age)
    assert status == 400


# проверим можно ли обновить данные о питомце с некорректным auth_key
@pytest.mark.invalid_key
@pytest.mark.positive_tests
def test_update_pet_info_with_invalid_auth_key_with_fixture(fixture_get_api_key_with_invalid_data, fixture_get_api_key):
    age = "5"
    name = "Kirill"
    animal_type = "Elefant"
    _, my_pets = pf.get_list_of_pets(fixture_get_api_key, "my_pets")
    status, result, response_head = pf.change_pet(fixture_get_api_key_with_invalid_data, pet_id=my_pets['pets'][0]['id'], name=name, animal_type=animal_type, age=age)
    assert status == 403


# проверим можно ли удалить данные о питомце
@pytest.mark.positive_tests
@pytest.mark.tests_with_photo
def test_successful_delete_pet_with_fixture_with_decorator(fixture_get_api_key):
    age = "1"
    name = "Yura_1"
    type = "python"
    photo = "D:\PycharmProjects\PetFriendsApiAutotests\images\8077750.png"
    status, result, response_head = pf.add_new_pet_with_photo(fixture_get_api_key, name, type, age, photo)
    status_delete, result_delete, response_head = pf.delete_pet(fixture_get_api_key, result["id"])
    assert status_delete == 200
