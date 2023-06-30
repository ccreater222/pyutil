from tencentcloud.sts.v20180813 import sts_client, models as sts_models
from tencentcloud.cam.v20190116 import cam_client, models as cam_models
from tencentcloud.common import credential, common_client
import traceback
import logging

log = logging.getLogger("cloudsecuryt.tencent.cam")


def getCallerIdentity(cred: credential.Credential) -> sts_models.GetCallerIdentityResponse:
    try:
        client = sts_client.StsClient(cred, "ap-guangzhou")
        req = sts_models.GetCallerIdentityRequest()
        resp = client.GetCallerIdentity(req)
    except:
        log.error(traceback.format_exc())
        return None
    return resp


def listPoliciesForUser(cred: credential.Credential, uin) -> cam_models.ListAttachedUserPoliciesResponse:
    try:
        client = cam_client.CamClient(cred, "ap-guangzhou")
        req = cam_models.ListAttachedUserPoliciesRequest()

        req.TargetUin = int(uin)
        req.Rp = 200
        resp = client.ListAttachedUserPolicies(req)
        return resp
    except:
        log.error(traceback.format_exc())


def listGroupsForUser(cred: credential, uin) -> cam_models.ListGroupsForUserResponse:
    try:
        client = cam_client.CamClient(cred, "ap-guangzhou")
        req = cam_models.ListGroupsForUserRequest()
        req.Uid = int(uin)
        req.Rp = 200
        resp = client.ListGroupsForUser(req)
        return resp
    except:
        log.error(traceback.format_exc())


def listPoliciesForGroup(cred: credential, group_id) -> cam_models.ListAttachedGroupPoliciesResponse:
    try:
        client = cam_client.CamClient(cred, "ap-guangzhou")
        req = cam_models.ListAttachedGroupPoliciesRequest()
        req.Rp = 200
        req.TargetGroupId = int(group_id)
        resp = client.ListAttachedGroupPolicies(req)
        return resp
    except:
        log.error(traceback.format_exc())


def listPermissions(cred: credential.Credential):
    resp = getCallerIdentity(cred)
    if resp == None:
        return None
    log.info(resp)
    user_type = resp.Type
    user_id = resp.UserId
    policies = []
    account_id = resp.AccountId
    root_types = ["root", "camuser"]
    if user_type.lower() in root_types:
        logging.info("you are root!!!")
    resp2 = listPoliciesForUser(cred, user_id)
    if resp2 != None:
        for policy in resp2.List:
            policies.append(policy)
    resp3 = listGroupsForUser(cred, user_id)
    if resp3 != None:
        for group in resp3.GroupInfo:
            resp4 = listPoliciesForGroup(cred, group.GroupId)
            if resp4 == None:
                continue
            for policy in resp4.List:
                policies.append(policy)
    return resp, policies
