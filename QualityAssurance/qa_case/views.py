from qa_case.models import CaseDetail
from qa_case import serializers
from rest_framework.views import APIView
from qa_common.models import UserInfo,BehaviorRecord
from rest_framework.response import Response
from django.db import connection
import datetime
from qa_common.extensions.jwt_auth import JwtAuthentication, create_token
from qa_common.code import code
from qa_common.extensions.pagination import LimitOffset

class CaseListView(APIView):
    authentication_classes = []
    """
    用例列表
    """
    def get(self,request,version_id,*args,**kwargs):
        case_query = CaseDetail.objects.filter(version_id=version_id)
        case_count = case_query.count()
        page_obj = LimitOffset()
        case_page = page_obj.paginate_queryset(queryset=case_query,request=request,view=self)
        case_list = serializers.CaseDetailSerializer(case_page,many=True)
        return Response({
            'total':case_count,
            'status':{'code':code.success_code[0],'msg':code.success_code[1]},
            'data':case_list.data
        })

class CaseDetailView(APIView):
    authentication_classes = []
    """
    用例详细信息
    """
    def get(self,request,case_id,*args,**kwargs):
        case_detail_query = CaseDetail.objects.get(case_id=case_id)
        case_detail = serializers.CaseDetailSerializer(case_detail_query)
        return Response({
            'status':{'code':code.success_code[0],'msg':code.success_code[1]},
            'data':case_detail.data
        })

class CaseManageView(APIView):
    authentication_classes = []
    """
    用例管理：新建、编辑、删除
    """
    def post(self,request,*args,**kwargs):
        time = datetime.datetime.now()
        behavior = BehaviorRecord(
            user_id=1,
            user_name="方圻程",
            behavior="新建用例",
            behavior_time=time
        )
        behavior.save()
        s = serializers.CaseDetailSerializer(data=request.data)
        try:
            duplicate_title = CaseDetail.objects.get(case_name=request.data['case_name'])
            return Response({
                "status":{'code':code.error_2006[0],'msg':code.error_2006[1]}
            })
        except:
            if s.is_valid():
                s.save()
                return Response({
                    "status":{'code':code.success_code[0],'msg':code.success_code[1]}
                })
    def put(self,request,*args,**kwargs):
        time = datetime.datetime.now()
        behavior = BehaviorRecord(
            user_id=1,
            user_name="方圻程",
            behavior="修改用例",
            behavior_time=time
        )
        behavior.save()
        s_query = CaseDetail.objects.get(case_id=request.data['case_id'])
        s = serializers.CaseDetailSerializer(data=request.data,instance=s_query)
        if s.is_valid():
            s.save()
            return Response({
                "status": {'code': code.success_code[0], 'msg': code.success_code[1]}
            })
    def delete(self,request,*args,**kwargs):
        time = datetime.datetime.now()
        behavior = BehaviorRecord(
            user_id=1,
            user_name="方圻程",
            behavior="删除用例",
            behavior_time=time
        )
        behavior.save()
        case_query = CaseDetail.objects.get(case_id=request.data['case_id'])
        case_query.delete()
        return Response({
            "status":{'code':code.success_code[0],'msg':code.success_code[1]}
        })
