from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator

translator = Translator()

class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()  # WYSIWYG Support
    question_hi = models.TextField(blank=True, null=True)  # Hindi Translation
    question_bn = models.TextField(blank=True, null=True)  # Bengali Translation

    def save(self, *args, **kwargs):
        # Auto-translate the question
        if not self.question_hi:
            self.question_hi = translator.translate(self.question, dest='hi').text
        if not self.question_bn:
            self.question_bn = translator.translate(self.question, dest='bn').text
        super().save(*args, **kwargs)

    def get_translated_question(self, lang='en'):
        if lang == 'hi' and self.question_hi:
            return self.question_hi
        elif lang == 'bn' and self.question_bn:
            return self.question_bn
        return self.question  # Default to English

    def __str__(self):
        return self.question
