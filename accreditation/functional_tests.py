from selenium import webdriver
import unittest
import time


def input_help_function(test, input_id, placeholder):
    inputbox = test.browser.find_element_by_id(input_id)
    test.assertEqual(
        inputbox.get_attribute('placeholder'),
        placeholder
    )
    inputbox.send_keys(test.name)


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox(executable_path=r'/Applications/geckodriver')

        # user info
        self.name = 'Emily'
        self.surname = 'Svensson'
        self.email = 'emily.svensson@test.com'

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # User goes to accreditation page
        self.browser.get('http://localhost:8000')

        # The title of page is accreditation
        self.assertIn('Accreditation', self.browser.title)

        # The header test says that the user can apply for accreditation
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Apply for Popaganda Accreditation', header_text)

        # The user sees an inputbox where she can enter first name
        input_help_function(self, 'id_first_name', 'First Name')

        # The user sees an inputbox where she can enter last name
        input_help_function(self, 'id_last_name', 'Last Name')

        # The user sees an inputbox where she can enter last name
        input_help_function(self, 'id_email', 'Email')

        # She clicks the send_button and then sees that the page updates to say
        # that her application will be reviewed and she will receive further info via email
        self.browser.find_element_by_id('send_button').click()
        time.sleep(1)

        information_to_the_user_div = self.browser.find_element_by_id('id_user_info')
        paragraph_text = information_to_the_user_div.find_elements_by_tag_name('p')
        self.assertTrue(
            self.name in paragraph_text.text
        )
        self.assertTrue(
            self.surname in paragraph_text.text
        )
        self.assertTrue(
            self.email in paragraph_text.text
        )

        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
