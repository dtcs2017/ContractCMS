from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from contracts.models import Contract
from .forms import PaymentForm
# from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.urls import reverse
from .models import Payment
from django.contrib.auth.decorators import login_required
from account.permission_decorator import accountant_only
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='cmslog.log',
                    filemode='a+')


@login_required
def payment_detail(request, contract_id):
    """
    根据合同ID返回指定合同的付款详情页
    页面内包含该合同的简要数据以及付款记录
    :param request:
    :param contract_id:
    :return:
    """
    if request.method == "GET":
        contract = get_object_or_404(Contract, id=contract_id)
        payments = contract.payments.all()
        form = PaymentForm()
        return render(request, 'payments/payment_detail.html',
                      {'contract': contract, 'payments': payments, 'form': form})
    else:
        if not request.user.is_accountant:
            return HttpResponse('不具备添加和修改付款权限，请返回上一页')

        contract = get_object_or_404(Contract, id=contract_id)
        payments = contract.payments.all()
        form = PaymentForm(request.POST)
        if form.is_valid():
            new_payment = form.save(commit=False)
            new_payment.contract = contract
            new_payment.save()
            logging.info("{} | payment_add | amount={} | id={} | rate={}".format(request.user.username, new_payment.amount,
                                                                       new_payment.id,new_payment.rate))
            messages.success(request, '成功添加付款记录')
            return redirect(reverse('payments:payment_detail', args=[contract.id]))
        else:
            return render(request, 'payments/payment_detail.html',
                          {"contract": contract, 'payments': payments, 'form': form})


@login_required
@accountant_only
def payment_edit(request, contract_id, payment_id):
    """
    编辑付款视图，仅财务部人员可操作
    :param request:request对象
    :param contract_id:合同id，URL参数
    :param payment_id:付款记录id，URL参数
    :return:
    """
    if request.method == "GET":
        contract = get_object_or_404(Contract, id=contract_id)
        payment = get_object_or_404(Payment, id=payment_id)
        form = PaymentForm(instance=payment)
        return render(request, 'payments/payment_edit.html', {'contract': contract, 'form': form})

    else:
        contract = get_object_or_404(Contract, id=contract_id)
        payment = get_object_or_404(Payment, id=payment_id)
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            current_payment = form.save(commit=False)
            current_payment.contract = contract
            current_payment.save()
            logging.info("{} | payment_edit | amount={} | id={} | rate={}".format(request.user.username, current_payment.amount,
                                                                        current_payment.id,current_payment.rate))
            messages.success(request, '修改付款记录成功')

            return redirect(reverse('payments:payment_detail', args=[contract.id]))
        else:
            return render(request, 'payments/payment_detail.html', {'contract': contract, 'form': form})
