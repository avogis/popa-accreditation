from selenium import webdriver
import unittest
import time


def input_help_function(test, input_id, placeholder, fomr_input):
    inputbox = test.browser.find_element_by_id(input_id)
    test.assertEqual(
        inputbox.get_attribute('placeholder'),
        placeholder
    )
    inputbox.send_keys(fomr_input)


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox(executable_path=r'/Applications/geckodriver')

        # user info
        self.name = 'Emily'
        self.surname = 'Svensson'
        self.email = 'emily.svensson@test.com'
        self.type_of_accreditation = 'photo'
        self.application = 'I am photographer'

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
        input_help_function(self, 'id_first_name', 'First Name', self.name)

        # The user sees an inputbox where she can enter last name
        input_help_function(self, 'id_last_name', 'Last Name', self.surname)

        # The user sees an inputbox where she can enter the reason for application
        select_box = self.browser.find_element_by_id('type_of_accreditation')
        options = [x.text for x in select_box.find_elements_by_tag_name('option')]
        expected_option = ['', 'Photo Pass', 'Festival Pass', 'Journalist Pass']
        for i in range(len(options)):
            self.assertEqual(expected_option[i], options[i])
        self.browser.find_element_by_id('photo').click()

        # The user sees an inputbox where she can enter the reason for application
        input_help_function(self, 'id_application', 'Futher information', self.application)

        # The user sees an inputbox where she can enter email
        input_help_function(self, 'id_email', 'Email', self.email)

        # The user agrees to terms and conditions
        self.browser.find_element_by_id("id_terms").click()

        # She clicks the send_button and then sees that the page updates to say
        # that her application will be granted and she will receive further info via email
        self.browser.find_element_by_id('send_button').click()
        time.sleep(1)

        information_to_the_user_div = self.browser.find_element_by_id('id_user_info').text
        self.assertTrue(
            self.name in information_to_the_user_div
        )
        self.assertTrue(
            self.surname in information_to_the_user_div
        )
        self.assertTrue(
            self.email in information_to_the_user_div
        )
        self.assertTrue(
            self.type_of_accreditation in information_to_the_user_div
        )
        self.assertTrue(
            self.application in information_to_the_user_div
        )


if __name__ == '__main__':
    unittest.main(warnings='ignore')
