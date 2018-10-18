.class public Lcom/flareon/flare/MainActivity;
.super Landroid/support/v7/app/ActionBarActivity;
.source "MainActivity.java"


# static fields
.field public static final EXTRA_MESSAGE:Ljava/lang/String; = "com.flare_on.flare.MESSAGE"


# direct methods
.method public constructor <init>()V
    .locals 0

    .prologue
    .line 10
    invoke-direct {p0}, Landroid/support/v7/app/ActionBarActivity;-><init>()V

    return-void
.end method


# virtual methods
.method protected onCreate(Landroid/os/Bundle;)V
    .locals 1
    .param p1, "savedInstanceState"    # Landroid/os/Bundle;

    .prologue
    .line 15
    invoke-super {p0, p1}, Landroid/support/v7/app/ActionBarActivity;->onCreate(Landroid/os/Bundle;)V

    .line 16
    const v0, 0x7f040019

    invoke-virtual {p0, v0}, Lcom/flareon/flare/MainActivity;->setContentView(I)V

    .line 17
    return-void
.end method

.method public validateEmail(Landroid/view/View;)V
    .locals 4
    .param p1, "view"    # Landroid/view/View;

    .prologue
    .line 21
    new-instance v2, Landroid/content/Intent;

    const-class v3, Lcom/flareon/flare/ValidateActivity;

    invoke-direct {v2, p0, v3}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 22
    .local v2, "intent":Landroid/content/Intent;
    const v3, 0x7f0c004f

    invoke-virtual {p0, v3}, Lcom/flareon/flare/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object v1

    check-cast v1, Landroid/widget/EditText;

    .line 23
    .local v1, "emailAddress":Landroid/widget/EditText;
    invoke-virtual {v1}, Landroid/widget/EditText;->getText()Landroid/text/Editable;

    move-result-object v3

    invoke-virtual {v3}, Ljava/lang/Object;->toString()Ljava/lang/String;

    move-result-object v0

    .line 24
    .local v0, "email":Ljava/lang/String;
    const-string v3, "com.flare_on.flare.MESSAGE"

    invoke-virtual {v2, v3, v0}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;

    .line 25
    invoke-virtual {p0, v2}, Lcom/flareon/flare/MainActivity;->startActivity(Landroid/content/Intent;)V

    .line 26
    return-void
.end method
