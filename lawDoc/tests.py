from django.test import TestCase,Client

class SearchTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_AllFeildSearch(self):
        print('-----------------------------------test_AllFeildSearch-----------------------------------')
        session = self.client.session
        session['allowed_count'] = 999
        session.save()
        response = self.client.post('/indexsearch', {'keyword': '杀'})
        print(response.status_code)
        self.assertEqual(response.status_code,200)
        count = response.context['resultCount']
        self.assertEqual(count, 11150)
        print('\n\n\n')

    def test_AllFeildNotSearch(self):
        print('-----------------------------------test_AllFeildNotSearch-----------------------------------')
        session = self.client.session
        session['allowed_count'] = 999
        session.save()
        response = self.client.post('/indexsearch', {'keyword': '!故意'})
        print(response.status_code)
        self.assertEqual(response.status_code,200)
        count = response.context['resultCount']
        self.assertEqual(count, 225568)
        print('\n\n\n')

    def test_OneFeildSearch(self):
        print('-----------------------------------test_OneFeildSearch-----------------------------------')
        session = self.client.session
        session['allowed_count'] = 999
        session.save()
        response = self.client.post('/indexsearch', {'keyword': '故意杀人@本院认为'})
        print(response.status_code)
        self.assertEqual(response.status_code,200)
        count = response.context['resultCount']
        self.assertEqual(count, 1442)
        print('\n\n\n')

    def test_OneFeildNotSearch(self):
        print('-----------------------------------test_OneFeildNotSearch-----------------------------------')
        session = self.client.session
        session['allowed_count'] = 999
        session.save()
        response = self.client.post('/indexsearch', {'keyword': '!故意杀人@本院认为'})
        print(response.status_code)
        self.assertEqual(response.status_code,200)
        count = response.context['resultCount']
        self.assertEqual(count, 298558)
        print('\n\n\n')

    def test_OrderSearch(self):
        print('-----------------------------------test_AllFeildSearch-----------------------------------')
        session = self.client.session
        session['allowed_count'] = 999
        session.save()
        response = self.client.post('/indexsearch', {'keyword': '杀人>分尸'})
        print(response.status_code)
        self.assertEqual(response.status_code,200)
        count = response.context['resultCount']
        self.assertEqual(count, 9)
        print('\n\n\n')

    def test_FieldSearch(self):
        print('-----------------------------------test_FeildSearch-----------------------------------')
        session = self.client.session
        session['allowed_count'] = 999
        session.save()
        response = self.client.post('/indexsearch', {'keyword': '第五十二条~第五十三条'})
        print(response.status_code)
        self.assertEqual(response.status_code,200)
        count = response.context['resultCount']
        self.assertEqual(count, 53463)
        print('\n\n\n')



