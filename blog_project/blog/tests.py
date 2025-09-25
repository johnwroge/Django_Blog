from django.test import TestCase

from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from blog.models import BlogPost, Comment

class BlogTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        # Create users
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )
        
        self.author_user = User.objects.create_user(
            username='author',
            email='author@test.com',
            password='testpass123'
        )
        
        self.regular_user = User.objects.create_user(
            username='user',
            email='user@test.com',
            password='testpass123'
        )
        
        # Create Blog Authors group
        self.blog_authors_group, created = Group.objects.get_or_create(name='Blog Authors')
        self.author_user.groups.add(self.blog_authors_group)
        
        # Create test blog post
        self.test_post = BlogPost.objects.create(
            title='Test Post',
            content='This is a test post content.',
            author=self.author_user,
            published=True
        )
        
        self.client = Client()

    def test_home_page_loads(self):
        """Test that home page loads and shows published posts"""
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_post_detail_loads(self):
        """Test individual post page loads"""
        response = self.client.get(reverse('blog:post_detail', kwargs={'pk': self.test_post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.test_post.title)

    def test_user_registration(self):
        """Test user can register"""
        response = self.client.post(reverse('blog:register'), {
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_login(self):
        """Test user can login"""
        response = self.client.post(reverse('login'), {
            'username': 'author',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login

    def test_post_creation_permissions(self):
        """Test only authors and superusers can create posts"""
        # Test regular user cannot access create post page
        self.client.login(username='user', password='testpass123')
        response = self.client.get(reverse('blog:post_create'))
        self.assertEqual(response.status_code, 302)  # Redirected (no permission)
        
        # Test author can access create post page
        self.client.login(username='author', password='testpass123')
        response = self.client.get(reverse('blog:post_create'))
        self.assertEqual(response.status_code, 200)
        
        # Test superuser can access create post page
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('blog:post_create'))
        self.assertEqual(response.status_code, 200)

    def test_post_creation(self):
        """Test creating a new post"""
        self.client.login(username='author', password='testpass123')
        response = self.client.post(reverse('blog:post_create'), {
            'title': 'New Test Post',
            'content': 'This is new post content.',
            'published': True
        })
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(BlogPost.objects.filter(title='New Test Post').exists())

    def test_comment_creation(self):
        """Test authenticated users can comment"""
        self.client.login(username='user', password='testpass123')
        response = self.client.post(reverse('blog:post_detail', kwargs={'pk': self.test_post.pk}), {
            'content': 'This is a test comment.'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after comment
        self.assertTrue(Comment.objects.filter(content='This is a test comment.').exists())

    def test_unauthenticated_comment_blocked(self):
        """Test unauthenticated users cannot comment"""
        response = self.client.post(reverse('blog:post_detail', kwargs={'pk': self.test_post.pk}), {
            'content': 'This should not work.'
        })
        # Should not create comment
        self.assertFalse(Comment.objects.filter(content='This should not work.').exists())

    def test_admin_access(self):
        """Test only superusers can access admin"""
        # Regular user cannot access admin
        self.client.login(username='user', password='testpass123')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)  # Redirected to login
        
        # Superuser can access admin
        self.client.login(username='admin', password='testpass123')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
