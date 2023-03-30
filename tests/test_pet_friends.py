import pytest
from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password, invalid_auth_key
import os

pf = PetFriends()


# 24.4.1
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверка того, что запрос API-ключа возвращает статус '200' и что результат содержит слово 'key"""

    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверка того, что запрос всех питомцев возвращает не пустой список.
    Перед этим происходит получение API-ключа и его сохранение в переменную 'auth_key'.
    Затем, при помощи этого ключа, происходит запрос списка всех питомцев и проверка того, что список не пустой.
    Доступное значение параметра 'filter' - 'my_pets' или ''' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Котенций', animal_type='Страшный',
                                     age='3', pet_photo='images/cat.jpg'):
    """Проверка что питомец с корректными данными добавляется"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверка того что мы можем удалить пета"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Кот", "программист", "1", "images/cat3.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Вовсе не кот', animal_type='мимик', age=2):
    """Првоерка того что мы можем обновить информацию о пете"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

# 27.7.2


def test_add_new_pet_without_photo(name='Кот', animal_type='Программист',
                                     age='1'):
    """Проверяем что можно добавить питомца с корректными данными без фото"""

    _,auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


def test_add_photo(pet_photo='images\cat3.jpg'):
    """Проверка добавления фото к уже существующему пету"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.set_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 200
        assert result['pet_photo']
    else:
        raise Exception('Пустой список с петами ')


def test_get_apikey_with_invalid_data(email=invalid_email, password=invalid_password):
    """Проверка того, что запрос API-ключа с не верными данными возвращает статус '403' и что результат не содержит слово 'key"""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result


def test_get_apikey_with_valid_email_and_invalid_password(email=valid_email, password=invalid_password):
    """Проверка того, что запрос API-ключа с частично верными данными возвращает статус '403' и что результат не содержит слово 'key"""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result


def test_get_apikey_without_data(email="_", password="_"):
    """Проверка того, что запрос API-ключа с пустыми данными возвращает статус '403' и что результат не содержит слово 'key"""
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result


def test_get_all_pets_with_incorrect_key(filter=''):
    """Проверка того, что запрос списка всех питомцев c некорректным значением API-ключа возвращает статус '403'"""

    status, result = pf.get_list_of_pets(invalid_auth_key, filter)

    assert status == 403

def test_add_pet_with_many_symb(name='Мурзик' *1000, animal_type='Соленый' *1000,
                                        age='2'*1000):
    """Проверка невозможности добавления пета с некорректным количеством символов"""
    #Тут происходит баг.Питомец добавляется.

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age,)

    assert status == 400

def test_add_new_pet_with_negative_age(name='А вдруг не кот', animal_type='Скрытень',
                                        age='-5', pet_photo='images/cat1.jpg'):
    """Проверка невозможности добавления питомца с отрицательным возрастом"""
    # Тут происходит баг.Питомец с отрицательным возрастом добавляется

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400
    assert result['age'] == age


def test_add_new_pet_with_empty_string(name='', animal_type='',
                                     age=''):
    """Проверка невозможности добавления питомца с отрицательным возрастом"""
    #Тут происходит баг.Питомец добавляется.

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 400
    assert result['name'] != name


def test_update_info_not_your_pet(name='Куст', animal_type='Забавный', age=10):
    """Проверка того что нельзя обновить информацию не своему пету"""
    #баг. Информация не своих петов обновляется

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, '')

    if len(all_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, all_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 400
        assert result['name'] == name
    else:
        raise Exception('Петов тут больше нет')
