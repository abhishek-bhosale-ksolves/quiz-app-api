from django.db import models
from users.models import User

class Quiz(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    time_limit = models.IntegerField()  # Time limit in minutes

    def __str__(self):
        return self.name

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.CharField(max_length=255)  # The correct answer

    def __str__(self):
        return self.question

class StudentAnswer(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)  # Student who gave the answer
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)  # Quiz for which the answer was given
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # Question being answered
    answer = models.CharField(max_length=255)  # Student's answer

    def __str__(self):
        return f'{self.student.username} - {self.quiz.name} - {self.question.question}'
    


class QuizResult(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.quiz.name}: {self.score}/{self.total_questions}"


