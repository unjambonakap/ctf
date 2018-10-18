.class public Lcom/flareon/flare/ValidateActivity;
.super Landroid/support/v7/app/ActionBarActivity;
.source "ValidateActivity.java"


# direct methods
.method static constructor <clinit>()V
    .locals 1

    .prologue
    .line 42
    const-string v0, "validate"

    invoke-static {v0}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V

    .line 43
    return-void
.end method

.method public constructor <init>()V
    .locals 0

    .prologue
    .line 14
    invoke-direct {p0}, Landroid/support/v7/app/ActionBarActivity;-><init>()V

    return-void
.end method


# virtual methods
.method protected onCreate(Landroid/os/Bundle;)V
    .locals 6
    .param p1, "savedInstanceState"    # Landroid/os/Bundle;

    .prologue
    .line 18
    invoke-super {p0, p1}, Landroid/support/v7/app/ActionBarActivity;->onCreate(Landroid/os/Bundle;)V

    .line 20
    new-instance v3, Landroid/widget/TextView;

    invoke-direct {v3, p0}, Landroid/widget/TextView;-><init>(Landroid/content/Context;)V

    .line 21
    .local v3, "textView":Landroid/widget/TextView;
    const/high16 v5, 0x42200000    # 40.0f

    invoke-virtual {v3, v5}, Landroid/widget/TextView;->setTextSize(F)V

    .line 22
    const/16 v5, 0x11

    invoke-virtual {v3, v5}, Landroid/widget/TextView;->setGravity(I)V

    .line 25
    invoke-virtual {p0}, Lcom/flareon/flare/ValidateActivity;->getIntent()Landroid/content/Intent;

    move-result-object v1

    .line 26
    .local v1, "intent":Landroid/content/Intent;
    const-string v5, "com.flare_on.flare.MESSAGE"

    invoke-virtual {v1, v5}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v4

    .line 27
    .local v4, "userInput":Ljava/lang/String;
    const-string v5, "US-ASCII"

    invoke-static {v5}, Ljava/nio/charset/Charset;->forName(Ljava/lang/String;)Ljava/nio/charset/Charset;

    move-result-object v5

    invoke-virtual {v5}, Ljava/nio/charset/Charset;->newEncoder()Ljava/nio/charset/CharsetEncoder;

    move-result-object v0

    .line 28
    .local v0, "asciiEnc":Ljava/nio/charset/CharsetEncoder;
    invoke-virtual {v0, v4}, Ljava/nio/charset/CharsetEncoder;->canEncode(Ljava/lang/CharSequence;)Z

    move-result v5

    if-eqz v5, :cond_0

    .line 30
    invoke-virtual {p0, v4}, Lcom/flareon/flare/ValidateActivity;->validate(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v2

    .line 31
    .local v2, "js":Ljava/lang/String;
    invoke-virtual {v3, v2}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 35
    .end local v2    # "js":Ljava/lang/String;
    :goto_0
    invoke-virtual {p0, v3}, Lcom/flareon/flare/ValidateActivity;->setContentView(Landroid/view/View;)V

    .line 36
    return-void

    .line 33
    :cond_0
    const-string v5, "No"

    invoke-virtual {v3, v5}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    goto :goto_0
.end method

.method public native validate(Ljava/lang/String;)Ljava/lang/String;
.end method
