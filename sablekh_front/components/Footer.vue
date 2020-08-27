<template>
    <div class="footer">
        <div class="links">
            <NuxtLink class = "bottom-link" to = "/privacy-policy">Privacy Policy</NuxtLink>
            <NuxtLink class = "bottom-link" to = "/terms-and-conditions">Terms and Conditions</NuxtLink>
        </div>
    </div>
</template>

<style scoped>
    .footer {
        padding: 10px 0;
    }
    .links {
        text-align: center;
    }
    .bottom-link {
        font-family: 'Staatliches', cursive;
        text-decoration: none;
        padding: 0 5vw;

    }
    .bottom-link:first-child {
        border-right: 2px solid black;
    }
</style>