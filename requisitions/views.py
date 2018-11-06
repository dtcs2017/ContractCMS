from django.shortcuts import render, get_object_or_404, redirect
from contracts.models import Contract
from .forms import RequisitionForm
from django.contrib import messages
from django.urls import reverse
from .models import Requisition
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='cmslog.log',
                    filemode='a')

@login_required
def requisition_detail(request, contract_id):
    """
    用于返回当前合同的详情和接受 POST 请求添加新记录
    :param request:
    :param contract_id:
    :return:
    """

    if request.method == "GET":
        contract = get_object_or_404(Contract, id=contract_id)
        reqs = contract.requisitions.all()
        form = RequisitionForm()
        return render(request, 'requisitions/req_detail.html', {"contract": contract, 'reqs': reqs, 'form': form})

    else:
        # if not (request.user.is_contractor or request.user.is_engineer):
        #     raise PermissionDenied
        contract = get_object_or_404(Contract, id=contract_id)
        reqs = contract.requisitions.all()
        form = RequisitionForm(request.POST)
        if form.is_valid():
            new_req = form.save(commit=False)
            new_req.contract = contract
            new_req.save()
            logging.info("{} | req_add | amount={} | id={}".format(request.user.username, new_req.amount, new_req.id))
            messages.success(request, '成功添加请款记录')
            return redirect(reverse('requisitions:req_detail', args=[contract.id]))
        return render(request, 'requisitions/req_detail.html', {"contract": contract, 'reqs': reqs, 'form': form})


@login_required
def requisition_edit(request, contract_id, req_id):
    if not (request.user.is_contractor or request.user.is_engineer):
        raise PermissionDenied

    if request.method == "GET":
        contract = get_object_or_404(Contract, id=contract_id)
        req = get_object_or_404(Requisition, id=req_id)
        form = RequisitionForm(instance=req)
        return render(request, 'requisitions/req_edit.html', {'contract': contract, 'form': form})

    else:
        contract = get_object_or_404(Contract, id=contract_id)
        req = get_object_or_404(Requisition, id=req_id)
        form = RequisitionForm(request.POST, instance=req)
        if form.is_valid():
            current_req = form.save(commit=False)
            current_req.contract = contract
            current_req.save()
            logging.info("{} | req_edit | amount={} | id={}".format(request.user.username, current_req.amount, current_req.id))
            messages.success(request, '修改请款记录成功')
            return redirect(reverse('requisitions:req_detail', args=[contract.id]))
        return render(request, 'requisitions/req_edit.html', {'contract': contract, 'form': form})
