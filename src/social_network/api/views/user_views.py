from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator

# from django.core.exceptions import ObjectDoesNotExist
# from django.db.models import Q

from social_user.models  import User
from ..serializers import UserRegistrationSerializer, UserSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users(request):
    """
    API endpoint to search users by email and name (paginated).

    - Requires authentication (`IsAuthenticated` permission class).
    - Accepts a single query parameter `search` for the search keyword.
    - Returns paginated results (up to 10 per page) based on search criteria.
    """
    search_term = request.GET.get('search', '')

    if not search_term:
        return Response({'error': 'Search keyword is required.'}, status=status.HTTP_400_BAD_REQUEST)

    if '@' in search_term and len(search_term) > 3:
        try:
            # Attempt exact email match first (case-insensitive)
            user = User.objects.get(email__iexact=search_term)
            serialized_user_data = UserSerializer(user)
            return Response(serialized_user_data.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            pass  # Continue searching by name if email match fails

    # Search for users with names containing the search term (case-insensitive)
    users = User.objects.filter(first_name__icontains=search_term)

    paginator = Paginator(users, 10)  # Paginate results with 10 per page
    page = request.GET.get('page')  # Allow pagination control through page parameter

    if int(page) > paginator.num_pages:
        return Response({'error': 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        paginated_users = paginator.page(page)
    except (ValueError, KeyError):
        return Response({'error': 'Invalid page number.'}, status=status.HTTP_400_BAD_REQUEST)

    serialized_data = UserSerializer(paginated_users, many=True)
    return Response(serialized_data.data, status=status.HTTP_200_OK)





@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):
    if request.user.is_authenticated:
        return Response({"detail": "User already logged in"}, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user:
            login(request, user)
            return Response({"detail": "Successfully logged in"}, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



        
