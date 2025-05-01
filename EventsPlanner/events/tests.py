# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import RegistrationForm 
from django.core import mail

class EventViewsTest(TestCase):

    def setUp(self):
        """Set up non-modified objects used by all test methods."""
        self.client = Client()
        # Create a test user for authenticated tests
        self.test_username = 'testuser'
        self.test_password = 'testpassword123'
        self.test_user = User.objects.create_user(
            username=self.test_username, 
            password=self.test_password
        )
        
        # Define URLs
        # Needed for redirect check
        self.index_url = reverse('index')
        self.signup_url = reverse('sign_up')
        self.logout_url = reverse('logout')
        self.login_url = reverse('login')
        self.contact_us_url = reverse('contact_us')
        self.past_events_url = reverse('past_events')
        self.upcoming_events_url = reverse('upcoming_events')

    # --- Tests for index view ---

    def test_index_view_authenticated_user(self):
        """Test index view is accessible for a logged-in user."""
        # Log the test user in
        self.client.login(username=self.test_username, password=self.test_password)
        
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/index.html')

    def test_index_view_unauthenticated_user_redirects_to_login(self):
        """Test index view redirects unauthenticated user to login page."""
        response = self.client.get(self.index_url)

        # Check for redirect status code (302) and correct redirect URL
        self.assertRedirects(response, f"{self.login_url}", target_status_code=200)
        # Or more simply if you don't need to check the 'next' param precisely:
        # self.assertEqual(response.status_code, 302)
        # self.assertTrue(response.url.startswith(self.login_url))


    # --- Tests for sign_up view ---

    def test_signup_view_get_request(self):
        """Test sign_up view renders the form correctly on GET."""
        response = self.client.get(self.signup_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/sign_up.html')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], RegistrationForm)
        # Check if the form is unbound (no data submitted yet)
        self.assertFalse(response.context['form'].is_bound)

    def test_signup_view_post_request_invalid_data(self):
        """Test sign_up view with invalid POST data re-renders the form with errors."""
        # Example: Assuming username and password are required, send empty data
        invalid_data = {} 
        response = self.client.post(self.signup_url, data=invalid_data)

        self.assertEqual(response.status_code, 200) # Should re-render, not redirect
        self.assertTemplateUsed(response, 'events/sign_up.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].is_bound) # Form should be bound
        self.assertTrue(response.context['form'].errors) # Form should have errors

    def test_signup_view_post_request_valid_data(self):
        """Test sign_up view with valid POST data creates user, logs in, and redirects."""
        
        # Prepare valid data - This depends HEAVILY on your RegistrationForm fields
        # Assuming standard UserCreationForm-like fields
        valid_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpassword123', 
            'password2': 'newpassword123',
            # Add other required fields from your RegistrationForm here
            # e.g., 'password2': 'newpassword123', 'email': 'new@example.com' 
        }
        
        # Check user count before POST
        user_count_before = User.objects.count()

        response = self.client.post(self.signup_url, data=valid_data)

        # Check user count after POST
        user_count_after = User.objects.count()
        self.assertEqual(user_count_after, user_count_before + 1)

        # Check if the new user exists
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
        # Check for redirect to index page
        self.assertRedirects(response, self.index_url, 
                             status_code=302, target_status_code=200) # Assumes index redirects if not logged in, but sign up logs in

        # Optional: Verify the user is logged in after signup
        # Make another request to a protected page (like index)
        # and check it doesn't redirect to login
        response_after_signup = self.client.get(self.index_url)
        self.assertEqual(response_after_signup.status_code, 200) 


    # --- Tests for log_out view ---
    
    def test_logout_view_renders_template(self):
        """Test log_out view renders the logout confirmation page."""
        # Note: Your current logout view *only* renders a template. 
        # It doesn't actually log the user out using django.contrib.auth.logout.
        # This test reflects the *current* code's behavior.
        
        # Doesn't matter if user is logged in or out for this view as written
        response = self.client.get(self.logout_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/logout.html')
        
        
    # --- Tests for contact_us view ---  
        
    def test_contact_us_view_renders_template(self):
        ''' Test contact_us view renders the contact page'''
        
        response = self.client.get(self.contact_us_url)
        
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'events/contact_us.html')
        
    # --- Tests for past_event view ---  
    def test_past_events_view_renders_template(self):
        '''Test past_event view renders the past event page'''
        response = self.client.get(self.past_events_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/past_events.html')

     # --- Tests for upcoming_event view ---  
    def test_upcoming_event_view_renders_template(self):
        '''Test upcoming_event view'''
        response = self.client.get(self.upcoming_events_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'events/upcoming_events.html')
        
    
class EmailTest(TestCase):
    
       # --- Tests for sending email if the conditions where right ---  
    def test_send_email(self):
            # Send message.
        mail.send_mail(
        "Subject here",
        "Here is the message.",
        "from@example.com",
        ["to@example.com"],
        fail_silently=False,
        )
        
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, "Subject here")
            
           
       
        
      
   
    # --- Suggestion for improved logout ---
    # If you intended the logout view to actually log the user out, 
    # you would modify the view to call `logout(request)` from `django.contrib.auth`
    # and then the test would look something like this:
    # 
    # from django.contrib.auth import SESSION_KEY
    # 
    # def test_logout_view_logs_user_out_and_redirects(self):
    #     """Test that the logout view logs the user out and redirects (Improved Version)."""
    #     # Log the user in first
    #     self.client.login(username=self.test_username, password=self.test_password)
    #     
    #     # Check user is logged in (session has auth key)
    #     self.assertIn(SESSION_KEY, self.client.session) 
    #     
    #     # Assuming the improved logout view calls logout() and redirects (e.g., to index or login)
    #     # response = self.client.get(self.logout_url, follow=True) # follow=True to follow the redirect
    #     response = self.client.get(self.logout_url) # If it redirects
    #
    #     # Check user is logged out (session no longer has auth key)
    #     self.assertNotIn(SESSION_KEY, self.client.session)
    #     
    #     # Check redirect (e.g., redirects to index, which then redirects to login)
    #     # self.assertRedirects(response, self.login_url + f"?next={self.index_url}") 
    #     # OR if it redirects directly to a 'logged out' page or login page:
    #     # self.assertRedirects(response, reverse('login')) # Or wherever it should go
