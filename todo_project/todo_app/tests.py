from django.test import TestCase
from django.urls import reverse
from faker import Faker
from django.contrib.auth.models import User
from todo_app.models import Todo
from django.contrib.auth import logout

class LoginTests(TestCase):
    def setUp(self):
        """Create a user with random username and password using Faker"""
        fake = Faker()
        self.username = fake.user_name()
        self.password = fake.password()
        self.user = User.objects.create_user(username=self.username,password=self.password)

    def test_login_page_loads(self):
        """to test the login page to load correctly"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_successful_login(self):
        """To test whether the login works with valid credentials"""  
        response = self.client.post(reverse('login'),{'username':self.username,'password':self.password})  
        self.assertRedirects(response, reverse('todo_list'))
    
    def test_login_form_has_required_elements(self):
        """Test if the login form contains all required elements"""
        response = self.client.get(reverse('login'))
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="password"')
        self.assertContains(response, 'type="submit"')
        self.assertContains(response, "Already Don't have an account? <a href=\"/signup/\">Sign up</a>")

    def test_signup_link_redirects_to_signup_page(self):
        """Test that clicking the 'Sign up' link redirects to the signup page"""
        response = self.client.get(reverse('login')) 
        signup_url = reverse('signup')
        response = self.client.get(signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html') 

class SignUpTests(TestCase):
    def setUp(self):
        """Create a user with random username and password using Faker"""
        fake = Faker()
        self.username = fake.user_name()
        self.password = fake.password()
        self.email = fake.email()

    def test_signup_page_loads(self):
        """Tests that the signup page loads correctly"""
        response = self.client.get(reverse('signup'))  # Replace with your actual signup URL
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')     

    def test_signup_form_has_required_elements(self):
        """Tests that the signup form contains all required fields"""
        response = self.client.get(reverse('signup'))
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="password1"')
        self.assertContains(response, 'name="password2"')
        self.assertContains(response, 'type="submit"')

    def test_successful_user_creation(self):
        """Tests that a user is created successfully with valid form data"""
        response = self.client.post(reverse('signup'), {
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password, 
        })
        self.assertRedirects(response, reverse('todo_list'))
        self.assertTrue(User.objects.filter(username=self.username).exists())


    def test_signup_form_valid(self):
        """Tests the signup form submission with valid data"""
        response = self.client.post(reverse('signup'), {
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password, 
        })
        self.assertRedirects(response, reverse('todo_list'))
        self.assertTrue(User.objects.filter(username=self.username).exists())
    
    def test_login_link_redirects_to_login_page(self):
        """Test that clicking the 'Login' link on the signup page redirects to the login page"""
        response = self.client.get(reverse('signup'))
        self.assertContains(response, '<a href="/login/">Login</a>')  # Check the link is present
        login_url = reverse('login')
        response = self.client.get(login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html') 

class TodoModel(TestCase):
    def setUp(self):
        """Create a test user and prepare for creating a todo task"""
        fake = Faker()
        self.username = fake.user_name()
        self.password = fake.password()
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)

    def test_todo_creation(self):
        """Test that a todo task can be created for a specific user using Faker."""
        fake = Faker()
        task_name = fake.sentence() 
        description = fake.text()  
        status = fake.random_element(["All", "In-Progress", "Completed"])

        todo = Todo.objects.create(
            user=self.user,
            task_name=task_name,
            description=description,
            status=status
        )
        self.assertEqual(todo.user.username, self.user.username) 
        self.assertEqual(todo.task_name, task_name)
        self.assertEqual(todo.description, description)
        self.assertEqual(todo.status, status)  

class TodoCreationTests(TestCase):
    def setUp(self):
        """Create a user and log them in for testing"""
        fake = Faker()
        self.username = fake.user_name()
        self.password = fake.password()
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)  

    def test_todo_creation(self):
        """Test that a todo task can be created from the todo list page with default status In-Progress"""
        fake = Faker() 
        task_name = fake.sentence()  
        description = fake.text() 

        response = self.client.post(reverse('todo_list'), {
            'task_name': task_name,
            'description': description,
        })
        self.assertRedirects(response, reverse('todo_list'))
        task = Todo.objects.get(task_name=task_name)
        self.assertEqual(task.status, 'In-Progress')
        self.assertTrue(Todo.objects.filter(task_name=task_name, description=description).exists())        
    
    def test_todo_form_submission(self):
        """Test that submitting the form on the todo list page actually creates a todo task"""
        fake = Faker() 
        task_name = fake.sentence()  
        description = fake.text() 

        response = self.client.post(reverse('todo_list'), {
            'task_name': task_name,
            'description': description,
        })
        self.assertRedirects(response, reverse('todo_list'))
        self.assertTrue(Todo.objects.filter(task_name=task_name).exists())
        self.assertTrue(Todo.objects.filter(description=description).exists())

    def test_task_display(self):
        """Test that tasks appear on the todo list with correct status"""
        fake = Faker()
        task_name = fake.sentence()
        description = fake.text()
        Todo.objects.create(user=self.user, task_name=task_name, description=description, status='In-Progress')
        response = self.client.get(reverse('todo_list'))
        self.assertContains(response, task_name)
        self.assertContains(response, 'In-Progress')
        self.assertContains(response, description)    

class LogoutTests(TestCase):
    def setUp(self):
        """Create a user and log them in for testing"""
        fake = Faker()
        self.username = fake.user_name()
        self.password = fake.password()
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)

    def test_logout_button_redirects_to_login(self):
        """Test that clicking the logout button logs the user out and redirects to login page"""
        response = self.client.post(reverse('logout')) 
        self.assertRedirects(response, reverse('login')) 

        response = self.client.get(reverse('todo_list'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('todo_list')}")

class TodoTabTests(TestCase):
    def setUp(self):
        """Create a test user and log them in"""
        fake = Faker()
        self.username = fake.user_name()
        self.password = fake.password()
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)

    def test_tabs_are_displayed(self):
        """Test that the tabs 'All', 'In-Progress', 'Completed' are displayed"""
        response = self.client.get(reverse('todo_list'))
        self.assertContains(response, "All")
        self.assertContains(response, "In-Progress")
        self.assertContains(response, "Completed")

    def test_filtering_by_tabs(self):
        """Test that tasks can be filtered by status (All, In-Progress, Completed)"""
        fake = Faker()
        Todo.objects.create(user=self.user, task_name=fake.sentence(), status="In-Progress")
        Todo.objects.create(user=self.user, task_name=fake.sentence(), status="Completed")

        # Test "All" tab
        response = self.client.get(reverse('todo_list') + '?status=All')
        self.assertContains(response, "In-Progress")
        self.assertContains(response, "Completed")

        # Test "In-Progress" tab
        response = self.client.get(reverse('todo_list') + '?status=In-Progress')
        self.assertContains(response, "In-Progress")
        # self.assertNotContains(response, "Completed")

        # Test "Completed" tab
        response = self.client.get(reverse('todo_list') + '?status=Completed')
        self.assertContains(response, "Completed")
        # self.assertNotContains(response, "In-Progress")

              