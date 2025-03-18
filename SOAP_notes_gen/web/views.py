from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import SOAPNote
from .llm import generate_subjective, generate_objective, generate_assessment, generate_plan

def index(request):
    return render(request, 'web/index.html')

@csrf_exempt
def save_conversation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        conversation = data.get('conversation')
        # Save conversation to database or process it
        return JsonResponse({'status': 'success'})

@csrf_exempt
def generate_soap(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        conversation = data.get('conversation')
        print(conversation)
        objective_stats = data.get('objective_stats')
        
        subjective = generate_subjective.invoke({"conversation": conversation})
        objective = generate_objective.invoke({
                            "conversation": conversation,
                            "subjective": subjective
                            })
        
        objective.content += f"\n\nAdditional Objective Data:\n{objective_stats}"

        assessment = generate_assessment.invoke({
                            "conversation": conversation,
                            "subjective": subjective,
                            "objective": objective
                            })
        plan = generate_plan.invoke({
                            "conversation": conversation,
                            "subjective": subjective,
                            "objective": objective,
                            "assessment": assessment
                            })
        
        return JsonResponse({
            'subjective': subjective.content,
            'objective': objective.content,
            'assessment': assessment.content,
            'plan': plan.content
        })

@csrf_exempt
def save_soap(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        soap_note = SOAPNote.objects.create(
            subjective=data.get('subjective'),
            objective=data.get('objective'),
            assessment=data.get('assessment'),
            plan=data.get('plan')
        )
        return JsonResponse({'status': 'success', 'id': soap_note.id})


