from django.test import TestCase
from .models import Editor,Article,tags
import datetime as dt

# Create your tests here.
class EditorTestClass(TestCase):
    # Setup method
    def setUp(self):
        self.collins = Editor(first_name = 'Collins', last_name = 'Akumu', email = 'akumucollins001@gmail.com')

    # Saving Editor Method
    def save_editor(self):
        self.save()

    # Deleting Editor Method
    def delete_editor(self):
        self.delete()

    # Updating the editor
    def update_editor():
        Editor.objects.filter(first_name=self.first_name).update(first_name=Collins)    
    
    # Display Editor
    def display_editor():
        editors = Editor.objects.all()
        return editors

    # Testing instance 
    def test_instance(self):
        self.assertTrue(isinstance(self.collins, Editor))    

    # Testing save method
    def test_save_method(self):
        self.collins.save_editor()
        self.assertTrue(len(editors)>0)   


class ArticleTestClass(TestCase):

    def setUp(self):
        # Creating a new editor and saving it
        self.collins= Editor(first_name = 'Collins', last_name ='Akumu', email ='akumucollins001@gmail.com')
        self.collins.save_editor()

        # Creating a new tag and saving it
        self.new_tag = tags(name = 'Mike Isaac')
        self.new_tag.save()

        self.new_article= Article(title = 'Sumter mirrors SC',post = 'News and buzz',editor = self.collins)
        self.new_article.save()

        self.new_article.tags.add(self.new_tag)

    # Deleting all instances of our models from the database after each test.
    def tearDown(self):
        Editor.objects.all().delete()
        tags.objects.all().delete()
        Article.objects.all().delete()

    def test_get_news_today(self):
            today_news = Article.todays_news()
            self.assertTrue(len(today_news)>0)

    def test_get_news_by_date(self):
        test_date = '2017-03-17'
        date = dt.datetime.strptime(test_date, '%Y-%m-%d').date()
        news_by_date = Article.days_news(date)
        self.assertTrue(len(news_by_date) == 0)        
        
