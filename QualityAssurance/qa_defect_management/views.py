from qa_defect_management.models import BugDetail,VersionDetail
from qa_defect_management import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
import datetime
from qa_common.extensions.jwt_auth import JwtAuthentication, create_token
from qa_common.code import code
from qa_common.extensions.pagination import LimitOffset

class BugListView(APIView):
    authentication_classes = []
    """
    BUG列表
    """
    def get(self,request,version_id,*args,**kwargs):
        bug_query = BugDetail.objects.filter(version_id=version_id)
        page_obj = LimitOffset()
        bug_page = page_obj.paginate_queryset(queryset=bug_query,request=request,view=self)
        bug_list = serializers.BugDetailSerializer(bug_page,many=True)
        return Response({
            'status':{'code':code.success_code[0],'msg':code.success_code[1]},
            'data':bug_list.data
        })

class BugDetailView(APIView):
    authentication_classes = []
    """
    BUG详细信息
    """
    def get(self,request,bug_id,*args,**kwargs):
        bug_detail_query = BugDetail.objects.get(id=bug_id)
        bug_detail = serializers.BugDetailSerializer(bug_detail_query)
        return Response({
            'status':{'code':code.success_code[0],'msg':code.success_code[1]},
            'data':bug_detail.data
        })