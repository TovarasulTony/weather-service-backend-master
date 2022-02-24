class CacheStruct:
  response_dict = {
    "id" : None,
    "city": None,
    "at" : None,
    "response" : None
  }
  CACHED_ELEMENTS_NO = 10
  next_id = 0
  oldest_id = 1
  request_list = []

  def check_request(self, city, at):
    for element in self.request_list:
      if element["city"] == city and element["at"] == at:
        return element["response"], True, None

    new_element = dict(self.response_dict)
    self.next_id += 1
    new_element["id"] = self.next_id
    new_element["city"] = city
    new_element["at"] = at
    self.request_list.append(new_element)
    if self.next_id - self.oldest_id > self.CACHED_ELEMENTS_NO:
      for element in self.request_list:
        if element["id"] == self.oldest_id:
          self.request_list.remove(element)
          self.oldest_id += 1
    return None, False, new_element["id"]

  def cache_response(self, id, response):
    for element in self.request_list:
      if element["id"] == id:
        element["response"] = response