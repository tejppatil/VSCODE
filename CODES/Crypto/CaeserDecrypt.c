#include<stdio.h>
#include<ctype.h>
int main(){
    char a[500],ch;
    int k;
    printf("Enter the encrypted text:");
    scanf("%s",a);
    printf("Enter the Key for Decryption:");
    scanf("%d",&k);
    for(int i=0;a[i]!='\0';i++){
        ch=a[i];
        if(ch){
            if(islower(ch)){
                ch=(ch-'a'-k)%26+'a';
            }
            if(isupper(ch)){
                ch=(ch-'A'-k)%26+'A';
            }
        }
        else{
            printf(":::::Invalid Message:::::");
        }
        a[i]=ch;
    }
    printf("Decrypted Message is: %s",a);
    return 0;
}