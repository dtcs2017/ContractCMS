from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import DirectCost, DirectRequisition, DirectPayment
from contracts.models import Subject
from .forms import DirectCostForm, DirectRequisitionForm, DirectPaymentForm
from django.contrib import messages
from django.urls import reverse
from account.permission_decorator import contractor_only, accountant_only
from django.contrib.auth.decorators import login_required

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='cmslog.log',
    filemode='a+')


# 非合同付款主体部分
@login_required
def minor_list(request, subject_id=None):
    subject = None
    if request.method == "GET":
        directcosts = DirectCost.objects.all()
        subjects = Subject.objects.all()
        if subject_id:
            subject = get_object_or_404(Subject, id=subject_id)
            directcosts = directcosts.filter(subject=subject)
        form = DirectCostForm()
        return render(request, 'minors/minors_list.html',
                      {'directcosts': directcosts, 'form': form, 'subjects': subjects, 'subject': subject})


@login_required
@contractor_only
def minor_add(request):
    if request.method == "POST":
        form = DirectCostForm(request.POST)
        if form.is_valid():
            new_minor = form.save()
            messages.success(request, '成功添加非合同记录')
            logging.info(
                "{} | minor_add | name={} | id={} | amount={}".format(
                    request.user, new_minor.supplier, new_minor.id, new_minor.amount,
                )
            )
            return redirect(reverse('minors:minor_list'))
        messages.error(request, '添加失败，请检查填写内容')
        return redirect(reverse('minors:minor_list'))

    else:
        return redirect(reverse('minors:minor_list'))


@login_required
@contractor_only
def minor_edit(request, directcost_id):
    if request.method == "GET":
        directcost = get_object_or_404(DirectCost, id=directcost_id)
        form = DirectCostForm(instance=directcost)
        return render(request, 'minors/minors_edit.html', {'form': form, 'directcost': directcost})
    else:
        directcost = get_object_or_404(DirectCost, id=directcost_id)
        form = DirectCostForm(request.POST, instance=directcost)
        if form.is_valid():
            current_directcost = form.save()
            messages.success(request, '成功修改非合同付款记录')
            logging.info(
                "{} | minor_edit | name={} | id={} | amount={}".format(
                    request.user, current_directcost.supplier, current_directcost.id, current_directcost.amount,
                )
            )
            return redirect(reverse('minors:minor_list'))
        messages.error(request, '修改失败，请检查填写内容')
        return render(request, 'minors/minors_edit.html', {'form': form, 'directcost': directcost})


# 非合同付款请款部分
@login_required
def req_list(request, directcost_id):
    if request.method == "GET":
        directcost = get_object_or_404(DirectCost, id=directcost_id)
        reqs = directcost.directreqs.all()
        form = DirectRequisitionForm()
        return render(request, 'minors/directreqs_list.html',
                      {'directcost': directcost, 'form': form, 'reqs': reqs})
    else:
        if request.user.is_accountant:
            return HttpResponse('不具备权限')
        directcost = get_object_or_404(DirectCost, id=directcost_id)
        reqs = directcost.directreqs.all()
        form = DirectRequisitionForm(request.POST)
        if form.is_valid():
            new_req = form.save(commit=False)
            new_req.cost_record = directcost
            new_req.save()
            messages.success(request, '成功添加请款记录')
            logging.info(
                "{} | direct_req_add | id={} | amount={} | invoice={}".format(
                    request.user, new_req.id, new_req.amount, new_req.invoice,
                )
            )
            return redirect(reverse('minors:req_list', args=[directcost.id]))
        messages.error(request, '添加失败，请检查填写内容')
        return render(request, 'minors/directreqs_list.html',
                      {'directcost': directcost, 'form': form, 'reqs': reqs})


@login_required
def req_edit(request, directcost_id, req_id):
    if request.user.is_accountant:
        return HttpResponse('不具备权限')
    if request.method == "GET":
        directcost = get_object_or_404(DirectCost, id=directcost_id)
        req = get_object_or_404(DirectRequisition, id=req_id)
        form = DirectRequisitionForm(instance=req)
        return render(request, 'minors/directreqs_edit.html', {'directcost': directcost, 'form': form, 'req': req})

    else:
        directcost = get_object_or_404(DirectCost, id=directcost_id)
        req = get_object_or_404(DirectRequisition, id=req_id)
        form = DirectRequisitionForm(request.POST, instance=req)
        if form.is_valid():
            current_req = form.save()
            messages.success(request, '成功修改非合同请款信息')
            logging.info(
                "{} | direct_req_edit | id={} | amount={} | invoice={}".format(
                    request.user, current_req.id, current_req.amount, current_req.invoice,
                )
            )
            return redirect(reverse('minors:req_list', args=[directcost.id]))
        messages.error(request, '修改失败，请检查填写内容')
        return render(request, 'minors/directreqs_edit.html', {'directcost': directcost, 'form': form, 'req': req})


# 非合同付款付款记录部分
@login_required
def directpayment_list(request, directcost_id):
    """
    用于列出列表和新增付款记录
    :param request:
    :param directcost_id:
    :return:
    """
    if request.method == "GET":
        directcost = get_object_or_404(DirectCost, id=directcost_id)
        payments = directcost.directpayments.all()
        form = DirectPaymentForm()
        return render(request, 'minors/directpays_list.html',
                      {'directcost': directcost, 'form': form, 'payments': payments})
    else:
        if not request.user.is_accountant:
            return HttpResponse('不具备相应权限')
        directcost = get_object_or_404(DirectCost, id=directcost_id)
        payments = directcost.directpayments.all()
        form = DirectPaymentForm(request.POST)
        if form.is_valid():
            new_payment = form.save(commit=False)
            new_payment.cost_record = directcost
            new_payment.save()
            messages.success(request, '成功添加非合同付款记录')
            logging.info(
                "{} | direct_payments_add | id={} | amount={} | rate={}".format(
                    request.user, new_payment.id, new_payment.amount, new_payment.rate,
                )
            )
            return redirect(reverse('minors:pay_list', args=[directcost.id]))
        messages.error(request, '添加失败，请检查填写内容')
        return render(request, 'minors/directpays_list.html',
                      {'directcost': directcost, 'form': form, 'payments': payments})


@login_required
@accountant_only
def pay_edit(request, directcost_id, pay_id):
    if request.method == "GET":
        directcost = get_object_or_404(DirectCost, id=directcost_id)
        payment = get_object_or_404(DirectPayment, id=pay_id)
        form = DirectPaymentForm(instance=payment)
        return render(request, 'minors/directpays_edit.html',
                      {'directcost': directcost, 'form': form, 'payment': payment})

    else:
        directcost = get_object_or_404(DirectCost, id=directcost_id)
        payment = get_object_or_404(DirectPayment, id=pay_id)
        form = DirectPaymentForm(request.POST, instance=payment)
        if form.is_valid():
            current_payment = form.save()
            messages.success(request, '成功修改非合同付款信息')
            logging.info(
                "{} | direct_pay_edit | id={} | amount={} | rate={}".format(
                    request.user, current_payment.id, current_payment.amount, current_payment.rate,
                )
            )
            return redirect(reverse('minors:pay_list', args=[directcost.id]))
        messages.error(request, '修改失败，请检查填写内容')
        return render(request, 'minors/directpays_edit.html',
                      {'directcost': directcost, 'form': form, 'payment': payment})
