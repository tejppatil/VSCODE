//A program for checkin the duplicate elements in array
#include<stdio.h>
int main()
{
    int n,i,j;
    printf("Enter the size of array: ");
    scanf("%d",&n);
    int a[n];
    printf("Enter the elements of array:\n");
    for(i=0;i<n;i++)
    {
        scanf("%d",&a[i]);
    }
    printf("Entered array is: ");
    for(i=0;i<n;i++)
    {
        printf("%d ",a[i]);
    }
    for(i=0;i<n;i++)
    {
        for(j=i+1;j<n;j++)
        {
            if(a[i]=a[j])    
            {
                printf("\n%d is Repeated in array",a[i]);  
            }
            
        }
    }     
}