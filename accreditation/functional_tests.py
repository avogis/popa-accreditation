from selenium import webdriver
import unittest
import time


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
        self.assertIn('Apply for Popaganda accreditation', header_text)

        # The user sees an inputbox where she can enter first name
        name_inputbox = self.browser.find_element_by_id('id_first_name')
        self.assertEqual(
            name_inputbox.get_attribute('placeholder'),
            'First name'
        )

        # She enters her name

        name_inputbox.send_keys(self.name)

        # She clicks the send_button and then sees that the page updates to say
        # that her application will be reviewed and she will receive further info via email
        self.browser.find_element_by_css_selector('.send_button').click()
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
