from django.core.exceptions import ValidationError
# from django.core.validators import MinValueValidator
from django.db.models import Q
# from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from social_user.models import FriendRequest, User, StatusChoices
from ..serializers import UserSerializer

class CustomRateThrottle(UserRateThrottle):
  rate="3/min"


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_friends(request):
  user = request.user
  pending = request.GET.get('pending', False)

  accepted_sent_requests = FriendRequest.objects.filter(
      from_user=user,
      status=StatusChoices.ACCEPTED if not pending else StatusChoices.PENDING
  ).values_list('to_user', flat=True)

  accepted_received_requests = FriendRequest.objects.filter(
      to_user=user,
      status=StatusChoices.ACCEPTED if not pending else StatusChoices.PENDING
  ).values_list('from_user', flat=True)

  if not accepted_sent_requests and not accepted_received_requests:
      return Response({'data': []}, status=status.HTTP_200_OK)

  if not accepted_sent_requests:
    friend_users = accepted_received_requests
  elif not accepted_received_requests:
    friend_users = accepted_sent_requests
  else:
    friend_users = accepted_sent_requests | accepted_received_requests

  friend_users= set(friend_users)
  
  # Get the list of friend user objects
  friends = User.objects.filter(pk__in=friend_users)
  
  serializer = UserSerializer(friends, many=True)

  return Response({'data': serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@throttle_classes([CustomRateThrottle])
@permission_classes([IsAuthenticated])
def send_friend_request(request, pk):
  to_user = User.objects.get(pk=pk)
  from_user = request.user

  if from_user == to_user:
    raise ValidationError({'detail': 'You cannot send a friend request to yourself'})
  # Check if users are already friends
  if from_user.friends.filter(pk=to_user.pk).exists():
    return Response({'error': 'You are already friends with this user'}, status=status.HTTP_400_BAD_REQUEST)

  # Check for existing pending request
  _, created = FriendRequest.objects.get_or_create(
    from_user = from_user, 
    to_user = to_user
  )
  if not created:
    return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)

  return Response({'message': 'Friend request sent successfully'}, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def respond_friend_request(request, pk, is_accept):
  if not isinstance(is_accept, int) and 0 <= is_accept < 2:
    return Response({'error': 'Invalid Input Action'}, status=status.HTTP_400_BAD_REQUEST)
  
  try:
    friend_request = FriendRequest.objects.get(pk=pk)

    try:
      friend_request.clean()
    except ValidationError as e:
      return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
  except FriendRequest.DoesNotExist:
    return Response({'error': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)

  if friend_request.to_user != request.user:
    return Response({'error': 'You cannot respond to this request'}, status=status.HTTP_403_FORBIDDEN)

  if is_accept:

    friend_request.status = StatusChoices.ACCEPTED
    friend_request.save()
    return Response({'message': 'Friend request accepted successfully'}, status=status.HTTP_200_OK)


  friend_request.delete()

  return Response({'message': 'Friend request rejected successfully'}, status=status.HTTP_200_OK)
