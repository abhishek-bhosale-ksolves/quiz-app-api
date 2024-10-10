from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Quiz, Question, QuizResult, StudentAnswer
from quiz.permissions import IsStudent
from .models import Question, Quiz
from .serializers import QuestionSerializer, QuizSerializer
from rest_framework import status
from django.views import View
from rest_framework import status

class HomeScreen(View):
    def get(self,request):
        return render(request,'index.html')

# class QuizListCreateView(generics.ListCreateAPIView):
#     queryset = Quiz.objects.all()
#     serializer_class = QuizSerializer

# class QuizDetailView(generics.RetrieveUpdateAPIView):
#     queryset = Quiz.objects.all()
#     serializer_class = QuizSerializer

class QuizListCreateView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsStudent]  # Restrict access to students only

class QuizDetailView(generics.RetrieveUpdateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsStudent]  # Restrict access to students only

class QuestionListCreateView(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        quiz_id = self.kwargs['quiz_id']
        return Question.objects.filter(quiz_id=quiz_id)

    def perform_create(self, serializer):
        quiz_id = self.kwargs['quiz_id']
        serializer.save(quiz_id=quiz_id)

class QuestionDetailView(generics.RetrieveUpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class AttendQuizView(APIView):
    # permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request, quiz_id):
        student = request.user  # The authenticated student
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({'message': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)

        answers = request.data  # Expecting a list of answers from the student
        score = 0  # Initialize score
        total_questions = quiz.questions.count()

        if not answers or len(answers) != total_questions:
            return Response({
                'message': 'You must answer all the questions.'
            }, status=status.HTTP_400_BAD_REQUEST)

        for answer_data in answers:
            question_id = answer_data.get('question_id')
            student_answer = answer_data.get('answer')

            # Check if the answer is provided
            if not student_answer:
                return Response({
                    'message': f'Missing answer for question ID {question_id}.'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Fetch the corresponding question
            try:
                question = Question.objects.get(id=question_id, quiz=quiz)
            except Question.DoesNotExist:
                return Response({
                    'message': f'Question with ID {question_id} does not exist.'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Save the student's answer
            StudentAnswer.objects.create(
                student=student,
                quiz=quiz,
                question=question,
                answer=student_answer
            )

            if len(student_answer)==5:
                score += 1

        # Save the student's score in QuizResult model
        QuizResult.objects.create(
            student=student,
            quiz=quiz,
            score=score,
            total_questions=total_questions
        )

        return Response({
            'message': 'Quiz submitted successfully!',
            'score': score,
            'total_questions': total_questions,
            'correct_answers': score,
            'wrong_answers': total_questions - score
        }, status=status.HTTP_200_OK)

class ScoreView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, quiz_id):
        student = request.user  # The authenticated student
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({'message': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)

        # Fetch the stored result for this student and quiz
        try:
            quiz_result = QuizResult.objects.get(student=student, quiz=quiz)
        except QuizResult.DoesNotExist:
            return Response({
                'message': 'You have not attended this quiz.'
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'message': 'Score retrieved successfully!',
            'score': quiz_result.score,
            'total_questions': quiz_result.total_questions,
            'correct_answers': quiz_result.score,
            'wrong_answers': quiz_result.total_questions - quiz_result.score
        }, status=status.HTTP_200_OK)